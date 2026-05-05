## Fill the Pane — Version Changelog

**v0.5.41** *(current)*
- Debug log checkbox added to title bar, off by default

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

**v0.5.11** *(session baseline)*
- Starting point for this development session
- Window height set to 940px matching reference screenshot
- Vertical resize locked
- Graph title states: Warming Up, Test in Progress, Complete — Generating Graph
- Save/load messages show full path with Saved/Loaded prefix


**v0.5.10
- All saved/loaded messages (graph, animation, data, infographic) moved to dedicated label above graph area
- New message replaces old — unified location
- Infographic HTML: XMAX now declared as JS constant — curve and dots now render correctly
- Animation y-axis locked to final max from frame 1 — no more jumping/twitching


**v0.5.9 (built without go — skip)
- Animation y-axis fix via fixed_ymax parameter (superseded by v0.5.10)


**v0.5.8
- get_drives() now uses _drive_label() — dropdown shows C: 83% (788/952 GB) format
- Results rows: baseline alignment for label, value, unit
- Drive Info: separator lines removed, tighter row spacing (pady=2)
- Results: separator lines removed, tighter row spacing
- Status bar: no longer shows results summary after test
- Data Saved/Loaded messages moved to graph subtitle area


**v0.5.7
- Animation completely rewritten: frames generated at export time, not during test
- No frame capture during test — eliminates memory overhead
- Works identically for live data and loaded CSV
- Drive Info & Results: separator lines removed, tighter spacing
- ExportDialog: save location pre-filled on open
- Status bar: removed results info, only shows action messages


**v0.5.6
- Fixed _status_var AttributeError crash on startup
- _status_var and _warmup_var properly initialised in __init__ before _build_ui


**v0.5.5
- Fixed _status_var initialisation order (attempted fix, superseded by v0.5.6)


**v0.5.4
- Light theme background changed to #F0F0F0 (Windows default / Rufus)
- Font sizes reduced to match Rufus: body 9pt, buttons 9pt, header 11pt bold
- Section headers: Rufus style — bold label + horizontal rule extending right
- Version number baseline-aligned with title
- Status bar moved from bottom of window to above Start Test button
- Drive dropdown format: C: 83% (788/952 GB) — no (X:\) or dash


**v0.5.3
- Toggle dark mode: clear pill with blue outline, solid white thumb on left
- Toggle light mode: solid blue pill, solid white thumb on right
- Drive Info card: Rufus style, no card border, separator lines, bottom-aligned stats
- Results card: Rufus style, separator lines, bottom-aligned stats
- Combobox: back to ttk with flat style


**v0.5.2
- All fonts changed to Segoe UI
- Toggle: transparent background composited onto window bg color
- Moon icon changed to 🌙 crescent
- Version number anchor="se" to baseline-align with Pane
- Moon/Sun icons center-aligned vertically
- Drive dropdown format C: 83% (788/952 GB)
- _sync_gb_entry: Target GB = (total × fill%) - used space
- _drive_free stored for accurate sync


**v0.5.1
- Toggle corners: fully transparent via PIL RGBA rendering
- Target Write formula fixed: (total × fill%) - used space
- Drive dropdown replaced ttk.Combobox with OptionMenu for color control
- Slider tick row: 0% removed, red used% label added centered over red zone
- Infographic xMx uses XMAX (full drive capacity)


**v0.5.0
- Toggle PNG images updated with new provided assets
- Version number reduced to size 10
- Moon (●) + toggle + sun (☀) layout in title bar, both always visible
- ExportDialog: save location pre-filled with results folder path
- Save Data: Excel and Numbers formats removed, CSV only via filedialog
- Infographic: opens with default results folder path
- languages.json: save_data icon (📊) removed


**v0.4.9
- Drive switch resets graph but keeps Notes field
- Custom canvas slider with red zone for used space
- _fill_min stored as _slider_used_pct for slider drawing
- Animation frames captured at consistent 12.8×7.2 inch size
- Notes embedded in animation frames


**v0.4.8
- Title bar: subtitle removed from content area
- Version inline with title at same baseline
- Saved graph notes: fig.text() at bottom, reliably included in bbox_inches
- Animation from loaded data: regenerates frames by replaying samples
- Infographic x axis: XMAX passed as JS constant
- Infographic notes: rendered in HTML output


**v0.4.7
- Toggle switch uses uploaded PNG files (toggle_off.png / toggle_on.png)
- All button icons hardcoded in _build_left — translations are plain text only
- Dropdown selected text color: black on accent blue
- icons stripped from all translation strings and languages.json


**v0.4.6
- CSV save fixed: Drive Total Bytes and Notes columns actually written to all rows
- Load CSV graph fix: x-axis max restored from Drive Total Bytes column
- Notes in saved graph image: fig.text() at bottom of figure


**v0.4.5
- CSV save rows: Drive Total Bytes and Notes columns added (header fix from v0.4.4)
- Load CSV: drive total and notes restored, plot objects reset for clean redraw


**v0.4.4
- Theme menu removed; inline dark/light toggle added to title bar
- Notes field added next to Write Speed Over Time header
- Notes included in graph title on completion, saved in CSV, restored on load
- Load CSV: x-axis restored from Drive Total Bytes, notes restored
- CSV columns: Drive Total Bytes and Notes added
- Window default height increased to 900px


**v0.4.3
- All hardcoded UI strings now go through self._() — section labels, card rows, axis labels, graph header, GB entry hint, peak annotation
- Chinese Simplified: fully translated including 5 new keys
- Save Data button: 💾 icon correctly placed
- fill_min changed from max(5%, used+5%) to max(1%, used+1%)
- languages.json included in package


**v0.4.2
- languages.json external translation file
- results/ folder created automatically beside exe on first launch
- All export dialogs default to results folder
- Temp file: _FtP_YYYYMMDD_HHMMSS.tmp with timestamp
- Leftover _FtP_*.tmp files cleaned at test start
- Save Data double icon removed


**v0.4.1
- Graph disappearing on click fixed: _on_axes_leave and _on_mouse_move reset plot objects and call _update_graph()


**v0.4.0
- After test: ETA replaced with total elapsed time in status line
- Graph disappearing on click: _canvas.draw() after crosshair removal


**v0.3.3
- _update_graph rewritten to use set_data() — no ax.cla() during live test
- Persistent plot objects: _plot_line, _plot_fill, _plot_peak, _plot_ax2
- Secondary % x axis created once per ax.cla() cycle using secondary_xaxis()
- Eliminates matplotlib axes accumulation that was throttling write speed


**v0.3.2
- Rolled back to working v0.3 upload as base
- Applied: 16:9 removed, refresh drives preserve selection, ETA, % tooltip, secondary % axis, early stop progress fix


**v0.3.1 (problematic — do not use)
- Warmup always runs; show_warmup toggle added
- on_progress(0, tb, 0) call introduced performance regression


**v0.3
- True CDM SEQ1M Q8T1 write method
  - Single thread, QUEUE_DEPTH=8 outstanding OVERLAPPED requests
  - FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH | FILE_FLAG_OVERLAPPED
  - VirtualAlloc for sector-aligned buffers
  - WaitForMultipleObjects + GetOverlappedResult
- Pre-warm: 8MB at end of file before measurement
- Non-Windows fallback: sequential buffered Q1T1
- Secondary % x axis on graph
- Graph no longer locked to 16:9
- ETA display in status line
- % in mouseover tooltip
- Refresh Drives preserves selection


**v0.2
- Write method: SEQ1M Q8T1 via ThreadPoolExecutor (pre-OVERLAPPED attempt)
- fill_min: max(5%, used+5%)
- Button icons left-aligned
- MP4 removed from animation export (GIF only)
- Infographic for Web export added (interactive HTML)


**v0.14
- About dialog: Build time removed
- Light mode: section labels use black (SEC_LBL theme key)
- Slider: visual range 0-100%, min = max(10%, used+1GB as %)
- math import added


**v0.13

Light mode: peak speed green, average orange, duration black
Fill target exceeds free space: Drive Info border highlighted red
Error message placed above Start Test button
Drive Info button removed
Load Data button added below Save Data — loads previous CSV, updates graph and stats
Export menu removed
Language flags changed to national flag emojis
About This Program added under About menu, linked to popup
Fill target slider: 0–100% visual, draggable 10–90%


**v0.12

Progress bar removed
Graph x axis changed to total drive capacity
Light/dark mode now persists across launches via settings.ini beside exe
Graph drawn at 16:9 ratio
Segoe UI Variable as default font on Windows
.spec and .py generated for every iteration


**v0.11

Published to https://github.com/jiyang1018/Fill_the_Pane
Theme menu added with Light Mode and Dark Mode options
Language menu: names displayed in native language, ISO 3-letter abbreviation
All text changed to AP-Style Title Case
All fonts changed to Inter Regular 400
Font scale defined: Title 24 bold, Small 10, Stat 15 bold, Unit 10, Btn 12 bold, Header 12 bold, Menu 10, Sec 10
X axis changed to drive capacity filled percentage; elapsed time moved to mouseover tooltip
Fill target exceeds free space: Start Test greyed out, Drive Info numbers highlighted red
License changed to GNU General Public License v3.0


**v0.1

App renamed to Fill the Pane
Subtitle changed to Sequential Write Torture Test
CrystalDiskInfo-style drive info acquisition
Drive Info popup button added
Export menu: Export Result as Image, Export Progress as Animation (GIF/MP4), Export Report (CSV/XLS/.numbers)
Language menu: 24 languages with national flags
About menu: build date/time, version, GPL license, author info, GitHub link
AP-Style Title Case for all UI text
Drive icon before dropdown, refresh icon on Refresh Drives button
Start Test green, Stop Test red
Save Graph Image button with image icon
Save Animation button with video icon
Save Data button (renamed from Save CSV Data) with spreadsheet icon
Progress bar shows capacity % in white text centered
Graph mouseover: vertical line at cursor, shows total write amount and % of full capacity
EOF
echo "Done"