## Fill the Pane v0.6.04 -- 2026-05-11

- Min speed marker added to graph, PNG, GIF, and HTML infographic — annotates the lowest sample point
- Average speed shown as a dashed horizontal line across the graph in all outputs, with callout label placed above the line after the last sample point
- Min MB/s added to Results panel and HTML infographic stats
- Y-axis now starts near the lowest data value instead of 0
- Peak renamed to Max throughout — graph annotation, Results panel, status bar, HTML infographic
- HTML infographic now shows the pre-existing used space as a pink block with a dashed vertical line, matching the in-app graph
- "peak" and "peak_annotation" i18n keys renamed to "max_speed" and "max_annotation" to prevent languages.json from overriding the Max label
- GIF option removed from Save Graph Image — PNG and JPG only
- Save Animation renamed to Save Graph Animation
- Notes text in PNG and GIF exports moved to top-left, aligned with the graph title row
- Window height increased from 885px to 905px to accommodate the new Min results row
- Bottom padding restored on Infographic button after height adjustment

---

## Fill the Pane v0.6.04 -- 2026-05-11

- Min speed marker added to graph, PNG, GIF, and HTML infographic — annotates the lowest sample point
- Average speed shown as a dashed horizontal line across the graph in all outputs, with callout label placed above the line after the last sample point
- Min MB/s added to Results panel and HTML infographic stats
- Y-axis now starts near the lowest data value instead of 0
- Peak renamed to Max throughout — graph annotation, Results panel, status bar, HTML infographic
- HTML infographic now shows the pre-existing used space as a pink block with a dashed vertical line, matching the in-app graph
- "peak" and "peak_annotation" i18n keys renamed to "max_speed" and "max_annotation" to prevent languages.json from overriding the Max label
- GIF option removed from Save Graph Image — PNG and JPG only
- Save Animation renamed to Save Graph Animation
- Notes text in PNG and GIF exports moved to top-left, aligned with the graph title row
- Window height increased from 885px to 905px to accommodate the new Min results row
- Bottom padding restored on Infographic button after height adjustment

---

# Fill the Pane — Changelog

---

**v0.6.04**
- Min speed marker added to graph, PNG, GIF, and HTML infographic — annotates the lowest sample point
- Average speed shown as a dashed horizontal line across the graph in all outputs, with callout label placed above the line after the last sample point
- Min MB/s added to Results panel and HTML infographic stats
- Y-axis now starts near the lowest data value instead of 0
- Peak renamed to Max throughout — graph annotation, Results panel, status bar, HTML infographic
- HTML infographic now shows the pre-existing used space as a pink block with a dashed vertical line, matching the in-app graph
- "peak" and "peak_annotation" i18n keys renamed to "max_speed" and "max_annotation" to prevent languages.json from overriding the Max label
- GIF option removed from Save Graph Image — PNG and JPG only
- Save Animation renamed to Save Graph Animation
- Notes text in PNG and GIF exports moved to top-left, aligned with the graph title row
- Window height increased from 885px to 905px to accommodate the new Min results row
- Bottom padding restored on Infographic button after height adjustment

**v0.6.03**
- HTML infographic now shows the pre-existing used space as a pink block with a dashed vertical line, matching the in-app graph

**v0.6.02**
- Graph now shows previously used drive space as a pink/red shaded block from x=0 to the test start position, with a dashed vertical line marking where writing began
- X-axis values offset by pre-existing used bytes so each sample plots at its true position on the full drive
- `Drive Used Bytes` column added to CSV export and read back on load — loaded CSVs with this column show the used-space block correctly

**v0.6.01**
- Replaced Python write loop with native C++ DLL (`ftp_loop.dll`) — zero interpreter overhead in hot path
- C++ loop uses IOCP (`CreateIoCompletionPort` + `GetQueuedCompletionStatus`) — OS wakes thread exactly on completion, no polling
- XOR-shift buffer fill replaces `rand()` — faster and produces incompressible pseudo-random data
- Prewarm expanded to 256 MB inside the C++ loop
- `ready_flag` shared Value added — child signals main process after prewarm completes before `t0` is set, eliminating cold-start ramp in sample 1
- Python loop retained as automatic fallback if `ftp_loop.dll` is not found
- `build_dll.bat` added — auto-detects MSVC or MinGW, installs MinGW via winget if neither is present
- Version bumped to 0.6.x to mark transition to C++/Python hybrid architecture

**v0.5.97**
- C++/Python hybrid introduced — `_write_process` tries to load `ftp_loop.dll` via ctypes first, falls back to Python loop if not found
- First version of `ftp_loop.cpp` — native write loop with `HasOverlappedIoCompleted` polling, 8 MB prewarm, XOR-shift buffer fill
- `ftp_loop.dll` bundled in PyInstaller spec via `datas`

**v0.5.96**
- `ready_flag = multiprocessing.Value('i', 0)` added — child sets it after prewarm completes
- Main process waits on `ready_flag` before setting `t0` (15s timeout, 5ms poll interval)
- Eliminates cold-start ramp: sample 1 now starts at full steady-state speed
- Debug log now emits `ready_flag=1, t0 set` to confirm timing

**v0.5.95**
- Prewarm moved inside `_write_process` — child writes 8 x 1 MB from offset 0 on its own file handle before the measured loop starts
- `bytes_written` not updated during prewarm so main process clock stays clean
- Slot state reset after prewarm; `next_off` reset to 0 so measured loop rewrites from offset 0
- Main-process write prewarm removed (was warming the wrong handle)

**v0.5.94**
- Write prewarm moved to main process file handle, writing from offset 0 instead of end of file
- Prewarm runs in daemon thread with 15s timeout; resets slot state after completion

**v0.5.93**
- Read prewarm added — sequential Q8T1 read pass over up to 16 GB before `t0`; did not improve write speed, removed in v0.5.94

**v0.5.92**
- `bytes_written.value` update decoupled from hot completion path — now updated every 8 completions (~8 MB) instead of every chunk
- Reduces shared-memory lock contention from ~4300 acquisitions/sec to ~540/sec

**v0.5.91**
- Replaced `WaitForMultipleObjects` in child with tight `HasOverlappedIoCompleted` polling — gain was marginal

**v0.5.90**
- Removed prewarm — child process reaches full speed within 1 second without it, eliminating 15s "Warming Up..." delay
- Replaced `WaitForMultipleObjects` with tight `HasOverlappedIoCompleted` polling in child write process

**v0.5.89**
- Removed `FILE_FLAG_WRITE_THROUGH` from child write process and prewarm handle — `WriteFile` now returns `ERROR_IO_PENDING` immediately, enabling full NVMe queue depth

**v0.5.88**
- Rewrote write loop using `multiprocessing` — hot write path now runs in a separate process with its own GIL and CPU core, eliminating Python GIL as throughput bottleneck
- Speed improved from ~1500 MB/s to ~4200 MB/s average
- `_write_process` defined at module level for pickle compatibility
- `freeze_support()` added at `__main__` entry point for PyInstaller
- Child process communicates bytes written via `multiprocessing.Value`
- Watchdog updated to call `wp.terminate()` on child process if stuck

**v0.5.87**
- Replaced polling loop with IOCP (`CreateIoCompletionPort` + `GetQueuedCompletionStatus`) — did not resolve speed gap

**v0.5.86**
- Measured speed via `next_offset` (issued bytes) instead of completed bytes — eliminated driver sub-completion counting issues but `SetFilePointerEx` proved unreliable on `NO_BUFFERING` overlapped handles

**v0.5.85**
- Reverted to `WriteFile` polling with `SetFilePointerEx(FILE_CURRENT)` for kernel-accurate measurement — `FILE_CURRENT` always returns 0 on `NO_BUFFERING` overlapped handles, producing no samples

**v0.5.84**
- Replaced APC write loop with `SetFilePointerEx` measurement — failed because file pointer not updated by overlapped I/O

**v0.5.83**
- Replaced polling loop with `WriteFileEx` + `SleepEx` APC completion loop — Python GIL blocked APC callbacks from firing during `SleepEx`

**v0.5.82**
- Byte counting reverted to `CHUNK` per completion — confirmed driver splits 1 MB writes into ~3 sub-completions causing `InternalHigh` and `GetOverlappedResult` to return partial counts

**v0.5.81**
- Fixed `UnboundLocalError` on `peak` variable — missing `peak = 0.0` initialization before main loop was crashing after exactly 1 sample every run

**v0.5.80**
- Used `GetOverlappedResult(bWait=True)` after `HasOverlappedIoCompleted` to get real byte count — driver fires completion after first sub-completion (~333 KB), not full 1 MB

**v0.5.79**
- Fixed graph not rendering after Stop — `_samples_ref`, `_peak_ref`, `_avg_ref`, `_elapsed_ref` now updated live every 0.5s so watchdog can call `on_done` with accumulated data

**v0.5.78**
- Byte counting changed to `CHUNK` per completion — `InternalHigh` confirmed returning partial counts (~1/3 of actual)

**v0.5.77**
- Removed file pre-allocation (`SetEndOfFile`) — was reserving full target size (500+ GB) immediately on disk
- Reverted byte counting to `ovl.InternalHigh`
- Watchdog now deletes temp file after `TerminateThread`
- Watchdog calls `on_done` with accumulated samples after `TerminateThread` so graph renders on Stop

**v0.5.76**
- Fixed `sleep(0.0001)` replacing `sleep(0)` to yield GIL without starving other threads
- Byte counting changed to `CHUNK` (first attempt — caused overcounting)

**v0.5.75**
- Changed main loop `sleep(0.005)` to `sleep(0)` to eliminate polling gap — caused GIL to never release, worker stuck with no samples

**v0.5.74**
- Restored `FILE_FLAG_WRITE_THROUGH`

**v0.5.73**
- Added file pre-allocation via `SetFilePointerEx` + `SetEndOfFile` before writes

**v0.5.72**
- Prewarm timeout increased from 5s to 15s

**v0.5.71**
- Fixed `tb` calculation — subtracted `used` bytes so target write matches UI display instead of writing full `total * fill_fraction`

**v0.5.70**
- Prewarm moved to daemon sub-thread with 5s timeout — worker thread stays responsive to Stop during prewarm blocking

**v0.5.69**
- Restored prewarm with 30s watchdog timeout — too long

**v0.5.68**
- Prewarm removed (first attempt) — drive started cold, speed low

**v0.5.67**
- Prewarm rewritten to issue one write at a time, checking `_stop` between each `WriteFile` call

**v0.5.66**
- Added `uac_admin=True` to PyInstaller spec — app now requests elevation on launch, required for `CancelIoEx` to work on some NVMe drivers

**v0.5.65**
- Watchdog calls `on_error("stopped")` after `TerminateThread` path to reset GUI from "Stopping..." to "Ready"

**v0.5.64**
- Watchdog uses `taskkill /F /T /PID` to kill entire process tree — `TerminateProcess` alone did not kill PyInstaller bootloader

**v0.5.63**
- Watchdog kills parent process (PyInstaller bootloader) before self via `os.getppid()` + `OpenProcess` + `TerminateProcess`

**v0.5.62**
- All `os._exit()` calls replaced with `TerminateProcess(GetCurrentProcess())` — `os._exit` only killed Python child, PyInstaller bootloader survived

**v0.5.61**
- `CancelIoEx` in watchdog moved to its own daemon thread — was blocking the watchdog thread after `TerminateThread`

**v0.5.60**
- Watchdog: after `TerminateThread`, runs `CancelIoEx` then `CloseHandle` with 1s timeout; falls back to `os._exit` if `CloseHandle` blocks

**v0.5.59**
- Watchdog upgraded — `TerminateThread` to kill blocked worker, then `CancelIoEx` + `CloseHandle` from watchdog thread
- `CloseHandle` given 1s timeout before forced exit

**v0.5.58**
- Added `FILE_ATTRIBUTE_TEMPORARY` and `FILE_FLAG_DELETE_ON_CLOSE` to `CreateFile` flags — attempt to prevent OS page cache flush on stop, unsuccessful, caused multi-minute cache drain

**v0.5.57**
- On stop path: skip `CloseHandle` and abandon handle instead — `CloseHandle` with pending buffered I/O blocked indefinitely

**v0.5.56**
- Removed `FILE_FLAG_NO_BUFFERING` — buffered I/O attempted to allow `CloseHandle` to discard write cache on stop, unsuccessful, OS still flushed cache for minutes

**v0.5.55**
- `QUEUE_DEPTH` reduced to 1 — attempt to limit in-flight I/O on stop, unsuccessful, drive firmware still queued writes

**v0.5.54**
- Removed `FILE_FLAG_WRITE_THROUGH` — with `WRITE_THROUGH`, writes committed irrevocably to NVMe firmware queue and could not be cancelled

**v0.5.53**
- `CancelIoEx` moved to daemon thread in `stop()` — was blocking the GUI thread on this driver
- Watchdog timeout reduced from 5s to 2s
- Added extra debug log points throughout stop sequence

**v0.5.52**
- Fixed `_collect(block=False)` — replaced `GetOverlappedResult(bWait=False)` with reading `ovl.InternalHigh` directly after `HasOverlappedIoCompleted` check, eliminating blocking kernel call in non-blocking path

**v0.5.51**
- Fixed `GetOverlappedResult(bWait=False)` blocking — replaced with `HasOverlappedIoCompleted` check (`ovl.Internal == STATUS_PENDING`), pure Python, zero kernel calls

**v0.5.50**
- Fixed `_hFile` truthiness check — `CancelIoEx` was not firing because `if self._hFile:` failed when handle value was falsy

**v0.5.49**
- Replaced `WaitForMultipleObjects` with `time.sleep(0.005)` polling — `WaitForMultipleObjects` with 50ms timeout blocked indefinitely on ADATA Legend 860 driver

**v0.5.48**
- Added watchdog thread (5s timeout then `os._exit(1)`) to force-kill process if worker does not exit after stop

**v0.5.47**
- Replaced `CancelIo` with `CancelIoEx` — `CancelIo` only cancels I/O from the calling thread

**v0.5.46**
- Added debug logging inside write loop

**v0.5.45**
- Added `CancelIo` call on stop path (first attempt at I/O cancellation)

**v0.5.44**
- Fixed stop race condition in main loop

**v0.5.43**
- Fixed stop race condition in prewarm/main loop transition

**v0.5.42**
- Fixed stop race condition during prewarm phase

**v0.5.41**
- Added Debug Log checkbox to title bar, off by default
- Window height set to 885px
- Added error popups for write failures

**v0.5.40**
- Debug log checkbox alignment fix — bottom-aligned with version number

**v0.5.39**
- Window height set to 885px to fit left panel content exactly

**v0.5.38**
- Window height hardcoded to eliminate gap below Infographic button

**v0.5.37**
- Window height derived from content via `winfo_reqheight`

**v0.5.36**
- Left panel width fix after `pack_propagate` toggle side effect

**v0.5.35**
- Removed `pack_propagate(False)` to allow content-driven height measurement

**v0.5.34**
- Window height sizing attempt using `winfo_reqheight` on left frame

**v0.5.33**
- Window height now derived from left panel content; graph fills remaining height

**v0.5.32**
- `_error_lbl` and `_error_var` removed entirely from left panel
- Syntax fix: `for` loop accidentally deleted by `sed`

**v0.5.31**
- Exceed-free-space warning moved to native Windows `messagebox.showwarning`

**v0.5.30**
- Left panel rebuilt as pure top-down flow — removed `side="bottom"` anchor, spacer frame, and `btn_bot` container
- Consistent 8px section spacing between Results and status/buttons

**v0.5.29**
- Spacing adjustment between Results box and Ready label

**v0.5.28**
- Fixed graph title reverting to "Waiting for Test..." or "Test in Progress..." on mouse hover/leave after test completion
- Tooltip cleanup no longer forces full axes redraw

**v0.5.27**
- "Ready." shown after stopping with no samples — no red error message
- Real errors shown as native Windows `messagebox.showerror` popup
- `_finish` clears error label on successful test completion

**v0.5.26**
- Fixed "Stopping..." stuck on screen after stopping during prewarm
- `return` inside `try` replaced with `break` so post-finally code runs and GUI callback fires

**v0.5.25**
- Prewarm moved inside `try` block so `finally` always handles cleanup

**v0.5.24**
- Granular debug logging inside `finally` to pinpoint hang location

**v0.5.23**
- `CancelIo` called before `CloseHandle` in `finally` when stopped, reducing flush delay

**v0.5.22**
- Prewarm drain replaced with `WaitForMultipleObjects` loop checking `_stop` every 50ms

**v0.5.21**
- Prewarm moved inside `try` block (first attempt)

**v0.5.20**
- Fixed early `return` before `try/finally` that caused "Stopping..." to hang when stopped during prewarm

**v0.5.19**
- Drain skipped on stop — `CloseHandle` in `finally` cancels pending I/O instead

**v0.5.18**
- Reverted `stop()` to simple `_stop.set()` — no `CancelIo` or `CloseHandle` from GUI thread
- Fixed runaway writes continuing after pressing Stop

**v0.5.17**
- Root cause fix: drain loop was calling `WaitForSingleObject` on events after `hFile` was already closed by `stop()`, blocking forever
- `stop()` simplified — events are dead after `CloseHandle`, drain skipped when stopped

**v0.5.16**
- Added debug logging to `ftp_debug.log` beside exe to diagnose Stop Test hang

**v0.5.15**
- UI layout refinements: button order, section header spacing, status label anchoring
- Bottom 5 export buttons use text color instead of accent blue
- Results section uses `FONT_SMALL` for compact style
- Button font bumped to 11pt

**v0.5.14**
- Drive Info and Results row padding adjustments
- Section header `pady` reduced for tighter layout

**v0.5.13**
- Body frame padding equalized on all sides
- Left/right panel margins reduced to match bottom padding

**v0.5.12**
- Fixed body frame padding — equal margins on all sides of panel boxes
- Infographic button bottom padding matched to left/right padding

**v0.5.11**
- Window height set to 940px matching reference screenshot
- Vertical resize locked
- Graph title states: Warming Up, Test in Progress, Complete
- Save/load messages show full path with Saved/Loaded prefix

**v0.5.10**
- All saved/loaded messages moved to dedicated label above graph area — new message replaces old, unified location
- Infographic HTML: XMAX now declared as JS constant — curve and dots render correctly
- Animation y-axis locked to final max from frame 1 — no more jumping/twitching

**v0.5.9**
- Animation y-axis fix via fixed_ymax parameter (superseded by v0.5.10)

**v0.5.8**
- `get_drives()` now uses `_drive_label()` — dropdown shows "C: 83% (788/952 GB)" format
- Results rows: baseline alignment for label, value, unit
- Drive Info: separator lines removed, tighter row spacing
- Status bar: no longer shows results summary after test
- Data Saved/Loaded messages moved to graph subtitle area

**v0.5.7**
- Animation completely rewritten — frames generated at export time, not during test
- No frame capture during test — eliminates memory overhead
- Works identically for live data and loaded CSV
- Drive Info and Results: separator lines removed, tighter spacing
- ExportDialog: save location pre-filled on open
- Status bar: removed results info, only shows action messages

**v0.5.6**
- Fixed `_status_var` AttributeError crash on startup
- `_status_var` and `_warmup_var` properly initialised in `__init__` before `_build_ui`

**v0.5.5**
- Fixed `_status_var` initialisation order (superseded by v0.5.6)

**v0.5.4**
- Light theme background changed to #F0F0F0 (Windows default)
- Font sizes reduced: body 9pt, buttons 9pt, header 11pt bold
- Section headers: bold label with horizontal rule extending right
- Version number baseline-aligned with title
- Status bar moved from bottom of window to above Start Test button
- Drive dropdown format: "C: 83% (788/952 GB)"

**v0.5.3**
- Toggle dark mode: clear pill with blue outline, solid white thumb on left
- Toggle light mode: solid blue pill, solid white thumb on right
- Drive Info card: no card border, separator lines, bottom-aligned stats
- Results card: separator lines, bottom-aligned stats

**v0.5.2**
- All fonts changed to Segoe UI
- Toggle: transparent background composited onto window bg color
- Version number anchor set to baseline-align with title
- Moon/Sun icons center-aligned vertically
- Drive dropdown format: "C: 83% (788/952 GB)"
- `_sync_gb_entry`: Target GB = (total x fill%) - used space
- `_drive_free` stored for accurate sync

**v0.5.1**
- Toggle corners: fully transparent via PIL RGBA rendering
- Target Write formula fixed: (total x fill%) - used space
- Drive dropdown replaced `ttk.Combobox` with `OptionMenu` for color control
- Slider tick row: 0% removed, red used% label added centered over red zone
- Infographic xMx uses XMAX (full drive capacity)

**v0.5.0**
- Toggle PNG images updated with new provided assets
- Version number reduced to size 10
- Moon and toggle and sun layout in title bar, both always visible
- ExportDialog: save location pre-filled with results folder path
- Save Data: CSV only via filedialog
- Infographic: opens with default results folder path

**v0.4.9**
- Drive switch resets graph but keeps Notes field
- Custom canvas slider with red zone for used space
- `_fill_min` stored as `_slider_used_pct` for slider drawing
- Animation frames captured at consistent 12.8x7.2 inch size
- Notes embedded in animation frames

**v0.4.8**
- Title bar: subtitle removed from content area, version inline at same baseline
- Saved graph notes: `fig.text()` at bottom, reliably included in `bbox_inches`
- Animation from loaded data: regenerates frames by replaying samples
- Infographic x axis: XMAX passed as JS constant
- Infographic notes: rendered in HTML output

**v0.4.7**
- Toggle switch uses uploaded PNG files (toggle_off.png / toggle_on.png)
- All button icons hardcoded in `_build_left` — translations are plain text only
- Dropdown selected text color: black on accent blue
- Icons stripped from all translation strings and languages.json

**v0.4.6**
- CSV save fixed: Drive Total Bytes and Notes columns actually written to all rows
- Load CSV graph fix: x-axis max restored from Drive Total Bytes column
- Notes in saved graph image: `fig.text()` at bottom of figure

**v0.4.5**
- CSV save rows: Drive Total Bytes and Notes columns added
- Load CSV: drive total and notes restored, plot objects reset for clean redraw

**v0.4.4**
- Theme menu removed; inline dark/light toggle added to title bar
- Notes field added next to Write Speed Over Time header
- Notes included in graph title on completion, saved in CSV, restored on load
- Load CSV: x-axis restored from Drive Total Bytes, notes restored
- Window default height increased to 900px

**v0.4.3**
- All hardcoded UI strings now go through `self._()` — section labels, card rows, axis labels, graph header, GB entry hint, peak annotation
- Chinese Simplified: fully translated including 5 new keys
- `fill_min` changed from max(5%, used+5%) to max(1%, used+1%)
- languages.json included in package

**v0.4.2**
- languages.json external translation file
- results/ folder created automatically beside exe on first launch
- All export dialogs default to results folder
- Temp file: `_FtP_YYYYMMDD_HHMMSS.tmp` with timestamp
- Leftover `_FtP_*.tmp` files cleaned at test start
- Save Data double icon removed

**v0.4.1**
- Graph disappearing on click fixed — `_on_axes_leave` and `_on_mouse_move` reset plot objects and call `_update_graph()`

**v0.4.0**
- After test: ETA replaced with total elapsed time in status line
- Graph disappearing on click: `_canvas.draw()` after crosshair removal

**v0.3.3**
- `_update_graph` rewritten to use `set_data()` — no `ax.cla()` during live test
- Persistent plot objects: `_plot_line`, `_plot_fill`, `_plot_peak`, `_plot_ax2`
- Secondary % x axis created once per `ax.cla()` cycle using `secondary_xaxis()`
- Eliminates matplotlib axes accumulation that was throttling write speed

**v0.3.2**
- Rolled back to working v0.3 as base
- Applied: refresh drives preserves selection, ETA, % tooltip, secondary % axis, early stop progress fix

**v0.3.1**
- Warmup always runs; show_warmup toggle added
- `on_progress(0, tb, 0)` call introduced performance regression (do not use)

**v0.3**
- True SEQ1M Q8T1 write method: single thread, QUEUE_DEPTH=8 outstanding OVERLAPPED requests
- `FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH | FILE_FLAG_OVERLAPPED`
- `VirtualAlloc` for sector-aligned buffers
- `WaitForMultipleObjects` + `GetOverlappedResult`
- Pre-warm: 8 MB at end of file before measurement
- Non-Windows fallback: sequential buffered Q1T1
- Secondary % x axis on graph
- Graph no longer locked to 16:9
- ETA display in status line
- % in mouseover tooltip
- Refresh Drives preserves selection

**v0.2**
- Write method: SEQ1M Q8T1 via ThreadPoolExecutor (pre-OVERLAPPED attempt)
- `fill_min`: max(5%, used+5%)
- Button icons left-aligned
- MP4 removed from animation export (GIF only)
- Infographic for Web export added (interactive HTML)

**v0.14**
- About dialog: Build time removed
- Light mode: section labels use black (`SEC_LBL` theme key)
- Slider: visual range 0-100%, min = max(10%, used+1GB as %)
- `math` import added

**v0.13**
- Light mode: peak speed green, average orange, duration black
- Fill target exceeds free space: Drive Info border highlighted red
- Error message placed above Start Test button
- Drive Info button removed
- Load Data button added below Save Data — loads previous CSV, updates graph and stats
- Export menu removed
- Language flags changed to national flag emojis
- About This Program added under About menu
- Fill target slider: 0-100% visual, draggable 10-90%

**v0.12**
- Progress bar removed
- Graph x axis changed to total drive capacity
- Light/dark mode persists across launches via settings.ini
- Graph drawn at 16:9 ratio
- Segoe UI Variable as default font on Windows

**v0.11**
- Published to GitHub
- Theme menu added with Light Mode and Dark Mode options
- Language menu: names displayed in native language, ISO 3-letter abbreviation
- All fonts changed to Inter Regular 400
- X axis changed to drive capacity filled percentage; elapsed time moved to mouseover tooltip
- Fill target exceeds free space: Start Test greyed out, Drive Info numbers highlighted red
- License changed to GNU General Public License v3.0

**v0.1**
- App renamed to Fill the Pane
- Subtitle changed to Sequential Write Torture Test
- Drive Info popup button added
- Export menu: Export Result as Image, Export Progress as Animation (GIF), Export Report (CSV)
- Language menu: 24 languages with national flags
- About menu: version, GPL license, author info, GitHub link
- Start Test green, Stop Test red
- Save Graph Image, Save Animation, Save Data buttons added
- Progress bar shows capacity % in white text centered
- Graph mouseover: vertical line at cursor, shows total write amount and % of full capacity
