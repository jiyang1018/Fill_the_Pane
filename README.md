# Fill the Pane — Sequential Write Torture Test

A Windows tool that stress-tests drive write performance over time, revealing SLC cache size, cache exhaustion speed, and sustained post-cache write speed.

## What Fill the Pane does

Fill the Pane writes sequentially to a drive until it reaches a target fill percentage, sampling write speed every 500 ms and plotting the full time-series graph live. This shows you three things CrystalDiskMark was not designed to show:

- **Where the SLC cache exhausts** — the GB or % capacity at which speed drops
- **How far it drops** — some drives fall 80%+ from peak to sustained speed
- **What sustained speed looks like** — the speed a drive maintains after the cache is gone

CrystalDiskMark is a great free benchmark and the standard tool for quick drive comparisons. FTP is not a replacement — it answers different questions.

## A note on sequential write speed vs CrystalDiskMark

FTP uses the same SEQ1M Q8T1 I/O pattern (1 MB sequential writes, queue depth 8, single thread) and the same direct unbuffered Windows I/O flags. However, because the internal implementation of any benchmark is not fully public, and because factors like test duration, file size, measurement timing, and driver interaction can all affect results, **the sequential write speed reported by FTP may differ from CrystalDiskMark**. Neither number is wrong — they reflect the conditions of their respective tests. For head-to-head drive comparisons, use the same tool consistently.

## Features

- **SEQ1M Q8T1** — 1 MB sequential writes, queue depth 8, single thread
- Native C++ write loop (`ftp_loop.dll`) for maximum throughput — falls back to Python if DLL not present
- Pre-warm phase conditions the NVMe write pipeline before measurement starts
- Graph shows previously used drive space as a shaded block so results are in full drive context
- Configurable write target — slider from 0–100% of free space, or manual GB entry
- Live write speed graph updated every 500 ms
- Interactive crosshair tooltip — GB written, % capacity, elapsed time, speed at cursor
- Max, average, and min MB/s annotations on graph with average dashed line
- Max, average, min MB/s and duration in Results panel
- Dark and light theme
- Multi-language support (English, German, French, Spanish, Japanese, Simplified Chinese, Korean)
- Stop test instantly at any time
- Export graph as PNG or JPG image
- Export animated GIF of test progression
- Export samples as CSV
- Load previously saved CSV for review
- Infographic for Web — embeddable interactive HTML chart
- Notes field on graph panel
- Debug log toggle (off by default)
- Random data writes to prevent hardware compression from skewing results

## Requirements

Python 3.13 or later.

```
pip install matplotlib psutil pillow pyinstaller
```

## Build the portable .exe

### Step 1 — Build the native write loop DLL (one time)

The C++ DLL provides the highest write throughput. Run `build_dll.bat` from the project root — it detects MSVC or MinGW automatically and installs MinGW via winget if neither is present.

```
build_dll.bat
```

This produces `ftp_loop.dll` in the project root. The app works without it (falls back to the Python loop) but runs faster with it.

### Step 2 — Place source in `latest\`

The build script reads the source file directly from `latest\`. Place the current `fill_the_pane_vX.X.XX.py` there before building. `build.bat` will copy it to `code\` for history and clean up any older versions from `latest\` automatically.

### Step 3 — Build the exe

```
pyinstaller fill_the_pane.spec
```

Or double-click `build.bat` — it verifies the source is in `latest\`, copies it to `code\`, builds the exe, and launches it automatically.

The finished executable will be in `dist\`. Copy it anywhere — no installation needed.

## Run directly (Python)

```
python latest\fill_the_pane_v*.py
```

## Sample Result

![Fill the Pane sample graph](assets/Sample%20Result.png)

![Fill the Pane animation](assets/Sample%20Result.gif)

<a href="https://htmlpreview.github.io/?https://github.com/jiyang1018/Fill_the_Pane/blob/main/assets/Sample%20Result.html" target="_blank">View interactive infographic</a>

## Notes

- Writes a temporary `_FtP_*.tmp` file to the target drive and deletes it when done or on stop.
- The app requests Administrator privileges automatically at launch via UAC prompt — this is required for direct unbuffered I/O on some drives.
- Random bytes are used to prevent hardware compression from skewing results.
- Never writes more than the configured target percentage of total drive capacity.
- The SLC cache cliff (if present) appears as a sudden speed drop partway through the test — this is expected drive behavior, not a bug.
