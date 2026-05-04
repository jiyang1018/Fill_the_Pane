## Fill the Pane — Feature List

**Core Test**
- Sequential write torture test (SEQ1M Q8T1) using Windows OVERLAPPED async I/O
- 8 outstanding write slots (queue depth 8, thread 1) matching CrystalDiskMark methodology
- Pre-warm phase before measurement to condition drive write cache
- Configurable write target: slider from 0–100% of free space, or manual GB entry
- Writes random data to prevent SSD compression optimizations

**Real-Time Monitoring**
- Live write speed graph updated per sample interval
- Progress bar showing bytes written vs target
- ETA display during test
- Peak and average MB/s, duration shown in Results panel

**Stop Test**
- Instant stop during main write phase
- Fast stop during prewarm (~50ms response)
- Clean teardown — no runaway writes, no stuck UI

**Graph**
- Write speed over time plotted against drive capacity written
- Secondary x-axis showing % of total drive capacity
- Interactive crosshair tooltip showing GB written, % written, elapsed time, speed at cursor
- Peak annotation with arrow
- Persists after test for review

**Export**
- Save graph as image (PNG)
- Save animated GIF of test progression
- Save test data as CSV
- Load previously saved CSV data for review
- Infographic for Web — embeddable HTML chart

**Drive Selection**
- Auto-detects all available drives with used/free space
- Refresh drives button
- Warns and disables Start if target exceeds free space

**UI**
- Dark and light theme toggle
- Multi-language support (English, German, French, Spanish, Japanese, Simplified Chinese, Korean)
- Notes field on graph panel
- Debug log toggle (off by default)
- Errors shown via native Windows dialog

**Platform**
- Windows native (OVERLAPPED I/O, sector-aligned buffers via VirtualAlloc)
- Non-Windows fallback (sequential buffered Q1T1)
- Distributable as single `.exe` via PyInstaller