/*
 * ftp_loop.cpp -- Fill the Pane native write loop  (v0.6.01)
 *
 * Changes from v0.5.97:
 *   - IOCP replaces HasOverlappedIoCompleted polling. The OS wakes this
 *     thread exactly when a completion arrives -- zero wasted spin cycles.
 *   - Deeper prewarm: 256 MB instead of 8 MB.
 *   - XOR-shift buffer fill replaces rand() -- much faster.
 *   - Explicit _WriteBarrier on bytes_written updates.
 *
 * Build (MSVC):
 *   cl /O2 /LD /EHsc ftp_loop.cpp /Fe:ftp_loop.dll
 *
 * Build (MinGW/GCC):
 *   g++ -O2 -shared -o ftp_loop.dll ftp_loop.cpp -lkernel32 -static-libgcc -static-libstdc++
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdlib.h>

extern "C" {

__declspec(dllexport) int ftp_write_loop(
    const wchar_t*    path,
    int64_t           total_bytes,
    int32_t           chunk,
    int32_t           queue_depth,
    volatile int32_t* stop_flag,
    volatile int64_t* bytes_written,
    volatile int32_t* ready_flag
) {
    /* Open file */
    HANDLE hFile = CreateFileW(
        path, GENERIC_WRITE, FILE_SHARE_READ, NULL,
        CREATE_ALWAYS, FILE_FLAG_OVERLAPPED | FILE_FLAG_NO_BUFFERING, NULL
    );
    if (hFile == INVALID_HANDLE_VALUE) return 1;

    /* Create IOCP -- associates hFile; completions queued here */
    HANDLE hIOCP = CreateIoCompletionPort(hFile, NULL, 1, 1);
    if (!hIOCP) { CloseHandle(hFile); return 2; }

    /* Allocate aligned write buffers, XOR-shift filled.
     * Random data prevents the NVMe controller's hardware compression from
     * inflating results -- the same reason FTP uses random data by default.
     * XOR-shift is ~100x faster than rand() and produces good pseudo-random
     * output; VirtualAlloc guarantees 4 KB alignment for FILE_FLAG_NO_BUFFERING. */
    void** bufs = (void**)malloc(queue_depth * sizeof(void*));
    if (!bufs) { CloseHandle(hIOCP); CloseHandle(hFile); return 3; }

    uint64_t xr = 0x123456789ABCDEF0ULL;
    for (int i = 0; i < queue_depth; i++) {
        bufs[i] = VirtualAlloc(NULL, chunk, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (!bufs[i]) {
            for (int j = 0; j < i; j++) VirtualFree(bufs[j], 0, MEM_RELEASE);
            free(bufs); CloseHandle(hIOCP); CloseHandle(hFile); return 4;
        }
        uint64_t* p = (uint64_t*)bufs[i];
        int words = chunk / 8;
        for (int w = 0; w < words; w++) {
            xr ^= xr << 13; xr ^= xr >> 7; xr ^= xr << 17;
            p[w] = xr;
        }
    }

    /* OVERLAPPED array -- hEvent NULL for IOCP */
    OVERLAPPED* ovls = (OVERLAPPED*)calloc(queue_depth, sizeof(OVERLAPPED));
    if (!ovls) {
        for (int i = 0; i < queue_depth; i++) VirtualFree(bufs[i], 0, MEM_RELEASE);
        free(bufs); CloseHandle(hIOCP); CloseHandle(hFile); return 5;
    }

    int64_t* slot_off = (int64_t*)malloc(queue_depth * sizeof(int64_t));
    if (!slot_off) {
        free(ovls);
        for (int i = 0; i < queue_depth; i++) VirtualFree(bufs[i], 0, MEM_RELEASE);
        free(bufs); CloseHandle(hIOCP); CloseHandle(hFile); return 6;
    }
    for (int i = 0; i < queue_depth; i++) slot_off[i] = -1;

    /* Issue helper */
    auto issue = [&](int slot, int64_t off) {
        ovls[slot].Internal     = STATUS_PENDING;
        ovls[slot].InternalHigh = 0;
        ovls[slot].Offset       = (DWORD)(off & 0xFFFFFFFFULL);
        ovls[slot].OffsetHigh   = (DWORD)((uint64_t)off >> 32);
        ovls[slot].hEvent       = NULL;
        slot_off[slot]          = off;
        DWORD written = 0;
        WriteFile(hFile, bufs[slot], (DWORD)chunk, &written, &ovls[slot]);
    };

    /* Prewarm: 256 MB from offset 0, IOCP-drained, unmeasured */
    const int64_t PREWARM_BYTES = 256LL * 1024 * 1024;
    if (!*stop_flag) {
        int64_t pw_off = 0;
        int64_t pw_inf = 0;
        for (int s = 0; s < queue_depth && pw_off < PREWARM_BYTES && !*stop_flag; s++) {
            issue(s, pw_off); pw_off += chunk; pw_inf++;
        }
        while (pw_inf > 0 && !*stop_flag) {
            DWORD bx = 0; ULONG_PTR key = 0; OVERLAPPED* pov = NULL;
            if (!GetQueuedCompletionStatus(hIOCP, &bx, &key, &pov, 5000)) break;
            pw_inf--;
            int slot = (int)(pov - ovls); slot_off[slot] = -1;
            if (pw_off < PREWARM_BYTES && !*stop_flag) {
                issue(slot, pw_off); pw_off += chunk; pw_inf++;
            }
        }
        for (int i = 0; i < queue_depth; i++) slot_off[i] = -1;
    }

    /* Signal main process: ready */
    *ready_flag = 1;

    /* Measured loop: IOCP blocks until completion, reissue immediately */
    int64_t next_off      = 0;
    int64_t total_written = 0;
    int64_t in_flight     = 0;
    const int64_t UPDATE_INTERVAL = (int64_t)chunk * 8;
    int64_t since_update  = 0;

    for (int s = 0; s < queue_depth && next_off < total_bytes && !*stop_flag; s++) {
        issue(s, next_off); next_off += chunk; in_flight++;
    }

    while (in_flight > 0 && !*stop_flag) {
        DWORD bx = 0; ULONG_PTR key = 0; OVERLAPPED* pov = NULL;
        if (!GetQueuedCompletionStatus(hIOCP, &bx, &key, &pov, 2000) || !pov) break;

        in_flight--;
        int slot       = (int)(pov - ovls);
        slot_off[slot] = -1;
        total_written += chunk;
        since_update  += chunk;

        if (since_update >= UPDATE_INTERVAL) {
            _WriteBarrier();
            *bytes_written = total_written;
            since_update = 0;
        }

        if (next_off < total_bytes && !*stop_flag) {
            issue(slot, next_off); next_off += chunk; in_flight++;
        }
    }

    *bytes_written = total_written;

    CancelIoEx(hFile, NULL);
    CloseHandle(hIOCP);
    CloseHandle(hFile);
    for (int i = 0; i < queue_depth; i++) VirtualFree(bufs[i], 0, MEM_RELEASE);
    free(bufs); free(ovls); free(slot_off);
    return 0;
}

} /* extern "C" */
