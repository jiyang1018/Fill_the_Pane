# Fill the Pane — Sequential Write Torture Test

A CrystalDiskMark-inspired sequential write tester for Windows that reveals SLC cache exhaustion and sustained write performance over time.

## Why Fill the Pane?

CrystalDiskMark's short test only measures burst speed — it misses the point where a flash drive exhausts its fast SLC cache and drops to raw NAND speed. Fill the Pane writes continuously until it fills a target percentage of the drive, showing you the full picture.

## Features

- **SEQ1M Q8T1** — same methodology as CrystalDiskMark (1MB sequential, queue depth 8, single thread)
- Configurable write target — slider from 0–100% of free space, or manual GB entry
- Pre-warm phase before measurement to condition drive write cache
- Live write speed graph updated in real time
- Interactive crosshair tooltip — GB written, % capacity, elapsed time, speed at cursor
- Peak MB/s annotation on graph
- Peak, average MB/s and duration in Results panel
- Dark and light theme
- Multi-language support (English, German, French, Spanish, Japanese, Simplified Chinese, Korean)
- Stop test instantly at any time
- Export graph as PNG image
- Export animated GIF of test progression
- Export samples as CSV
- Load previously saved CSV for review
- Infographic for Web — embeddable HTML chart
- Notes field on graph panel
- Debug log toggle (off by default)
- Native Windows error dialogs
- Random data writes to prevent SSD compression from skewing results

## Requirements

Python 3.12 recommended (Python 3.13 has known PyInstaller compatibility issues).

```
pip install matplotlib psutil pillow pyinstaller
```

## Build the portable .exe

```
pyinstaller fill_the_pane.spec
```

Or double-click `build.bat` — it builds, copies the exe to `latest\`, and launches it automatically.

The finished executable will be in `dist\`. Copy it anywhere — no installation needed.

## Run directly (Python)

```
python code\fill_the_pane_v*.py
```

## Notes

- Writes a temporary file to the drive root and deletes it when done or on stop.
- Run as Administrator if testing the C: drive, as Windows may restrict writes to the system drive root.
- Random bytes are used to prevent filesystem and hardware compression from skewing results.
- Never writes more than the configured target percentage of total drive capacity.