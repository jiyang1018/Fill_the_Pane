"""
DriveMark - Sequential Write Benchmark Tool
A CrystalDiskMark-style sequential write tester with live graph
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import time
import csv
import shutil
import platform
import datetime
import math

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

# ── Attempt psutil import ──────────────────────────────────────────────────
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ═══════════════════════════════════════════════════════════════════════════
#  Drive / partition helpers
# ═══════════════════════════════════════════════════════════════════════════

def get_drives():
    """Return list of (label, mountpoint, total_bytes, free_bytes)."""
    drives = []
    if HAS_PSUTIL:
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                label = f"{part.device}  ({part.mountpoint})  —  {_fmt_size(usage.total)} total, {_fmt_size(usage.free)} free"
                drives.append((label, part.mountpoint, usage.total, usage.free))
            except Exception:
                pass
    else:
        # Fallback: check common Windows drive letters
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            mp = f"{letter}:\\"
            if os.path.exists(mp):
                try:
                    total, used, free = shutil.disk_usage(mp)
                    label = f"{mp}  —  {_fmt_size(total)} total, {_fmt_size(free)} free"
                    drives.append((label, mp, total, free))
                except Exception:
                    pass
    return drives


def _fmt_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


# ═══════════════════════════════════════════════════════════════════════════
#  Benchmark worker
# ═══════════════════════════════════════════════════════════════════════════

CHUNK = 4 * 1024 * 1024   # 4 MB write chunks
MEASURE_INTERVAL = 0.5     # seconds between speed samples

class BenchmarkWorker(threading.Thread):
    """
    Writes a single large file to `target_dir` up to `fill_fraction` of drive
    capacity, sampling speed every MEASURE_INTERVAL seconds.

    Callbacks (called on worker thread, marshal to GUI with after()):
        on_progress(bytes_written, total_target, mb_per_sec)
        on_sample(elapsed_sec, mb_per_sec)
        on_done(samples, peak_mb, avg_mb, elapsed)
        on_error(msg)
    """

    def __init__(self, target_dir, fill_fraction,
                 on_progress, on_sample, on_done, on_error):
        super().__init__(daemon=True)
        self.target_dir = target_dir
        self.fill_fraction = fill_fraction
        self.on_progress = on_progress
        self.on_sample = on_sample
        self.on_done = on_done
        self.on_error = on_error
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.on_error(str(e))

    def _run(self):
        try:
            total, used, free = shutil.disk_usage(self.target_dir)
        except Exception as e:
            self.on_error(f"Cannot read disk usage: {e}")
            return

        target_bytes = int(total * self.fill_fraction)
        # Never exceed 98 % of free space as a safety guard
        target_bytes = min(target_bytes, int(free * 0.98))

        if target_bytes < CHUNK:
            self.on_error(
                f"Not enough free space on drive.\n"
                f"Free: {_fmt_size(free)}, needed: {_fmt_size(CHUNK)}"
            )
            return

        tmp_path = os.path.join(self.target_dir, "_drivetest_benchmark_.tmp")
        chunk_data = os.urandom(CHUNK)   # random bytes to defeat compression

        samples = []          # [(elapsed_sec, mb_per_sec), ...]
        bytes_written = 0
        start_time = time.perf_counter()
        interval_start = start_time
        interval_bytes = 0

        try:
            with open(tmp_path, "wb", buffering=0) as f:
                while bytes_written < target_bytes:
                    if self._stop_event.is_set():
                        break

                    remaining = target_bytes - bytes_written
                    write_size = min(CHUNK, remaining)
                    data = chunk_data[:write_size]

                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())

                    bytes_written += write_size
                    interval_bytes += write_size

                    now = time.perf_counter()
                    elapsed_interval = now - interval_start

                    if elapsed_interval >= MEASURE_INTERVAL:
                        mb_s = (interval_bytes / elapsed_interval) / (1024 * 1024)
                        total_elapsed = now - start_time
                        samples.append((total_elapsed, mb_s))
                        self.on_sample(total_elapsed, mb_s)
                        self.on_progress(bytes_written, target_bytes, mb_s)
                        interval_start = now
                        interval_bytes = 0

        except OSError as e:
            pass   # Disk full mid-write is acceptable; report what we have
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        if not samples:
            self.on_error("No data was collected. Drive may be too fast or too small.")
            return

        total_elapsed = time.perf_counter() - start_time
        peak = max(s[1] for s in samples)
        avg  = sum(s[1] for s in samples) / len(samples)
        self.on_done(samples, peak, avg, total_elapsed)


# ═══════════════════════════════════════════════════════════════════════════
#  Main Application Window
# ═══════════════════════════════════════════════════════════════════════════

BG       = "#0d0f14"
PANEL    = "#13161e"
CARD     = "#1a1e2a"
ACCENT   = "#00d4ff"
ACCENT2  = "#ff6b35"
TEXT     = "#e8eaf0"
SUBTEXT  = "#7a8099"
GREEN    = "#39d353"
WARN     = "#f0c040"
BORDER   = "#252a38"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_LABEL  = ("Courier New", 10)
FONT_SMALL  = ("Courier New", 9)
FONT_STAT   = ("Courier New", 14, "bold")
FONT_UNIT   = ("Courier New", 9)
FONT_BTN    = ("Courier New", 11, "bold")
FONT_HEADER = ("Courier New", 11, "bold")


class DriveMark(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("DriveMark  —  Sequential Write Benchmark")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(900, 640)

        self._worker = None
        self._samples = []
        self._running = False
        self._fill_var = tk.DoubleVar(value=90.0)
        self._drive_var = tk.StringVar()

        self._drives = []   # (label, mountpoint, total, free)

        self._build_ui()
        self._refresh_drives()
        self.after(200, self._center_window)

    # ── Layout ────────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 1060, 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # ── Title bar ──
        title_bar = tk.Frame(self, bg=BG, pady=10)
        title_bar.pack(fill="x", padx=20)

        tk.Label(title_bar, text="⬡ DRIVEMARK", font=FONT_TITLE,
                 fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(title_bar, text="  sequential write benchmark",
                 font=("Courier New", 11), fg=SUBTEXT, bg=BG).pack(side="left", pady=6)

        # ── Main layout: left panel + right graph ──
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 14))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # Left control panel
        left = tk.Frame(body, bg=PANEL, bd=0, relief="flat",
                        width=290, highlightthickness=1,
                        highlightbackground=BORDER)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        left.pack_propagate(False)
        self._build_left(left)

        # Right graph panel
        right = tk.Frame(body, bg=PANEL, highlightthickness=1,
                         highlightbackground=BORDER)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_graph(right)

        # ── Status bar ──
        self._status_var = tk.StringVar(value="Ready.")
        status = tk.Label(self, textvariable=self._status_var,
                          font=FONT_SMALL, fg=SUBTEXT, bg=BG, anchor="w")
        status.pack(fill="x", padx=22, pady=(0, 6))

    def _build_left(self, parent):
        pad = dict(padx=16, pady=6)

        # Section: Drive Select
        self._section_label(parent, "SELECT DRIVE")
        self._drive_menu = ttk.Combobox(parent, textvariable=self._drive_var,
                                         state="readonly", font=FONT_SMALL)
        self._drive_menu.pack(fill="x", **pad)
        self._style_combobox()

        btn_refresh = self._mk_btn(parent, "↺  Refresh Drives",
                                    self._refresh_drives, color=SUBTEXT)
        btn_refresh.pack(fill="x", padx=16, pady=(0, 10))

        # Section: Fill %
        self._section_label(parent, "FILL TARGET")
        fill_row = tk.Frame(parent, bg=PANEL)
        fill_row.pack(fill="x", **pad)
        self._fill_label = tk.Label(fill_row, text="90%", font=FONT_STAT,
                                     fg=ACCENT, bg=PANEL, width=5)
        self._fill_label.pack(side="right")
        tk.Label(fill_row, text="Write up to", font=FONT_SMALL,
                 fg=SUBTEXT, bg=PANEL).pack(side="left", pady=4)

        fill_slider = tk.Scale(parent, from_=10, to=90, orient="horizontal",
                               variable=self._fill_var, bg=PANEL,
                               fg=TEXT, troughcolor=CARD, activebackground=ACCENT,
                               highlightthickness=0, bd=0, sliderlength=18,
                               command=self._on_fill_change, font=FONT_SMALL)
        fill_slider.pack(fill="x", padx=16, pady=(0, 10))

        # Disk info card
        self._section_label(parent, "DRIVE INFO")
        self._info_frame = tk.Frame(parent, bg=CARD, highlightthickness=1,
                                     highlightbackground=BORDER)
        self._info_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._info_labels = {}
        for key in ("Total", "Free", "Target Write"):
            row = tk.Frame(self._info_frame, bg=CARD)
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=key, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD, width=12, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="—", font=FONT_SMALL, fg=TEXT,
                           bg=CARD, anchor="e")
            lbl.pack(side="right")
            self._info_labels[key] = lbl

        # Stats card
        self._section_label(parent, "RESULTS")
        stats_frame = tk.Frame(parent, bg=CARD, highlightthickness=1,
                                highlightbackground=BORDER)
        stats_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._stat_labels = {}
        for key, unit in (("Peak", "MB/s"), ("Average", "MB/s"), ("Duration", "sec")):
            row = tk.Frame(stats_frame, bg=CARD)
            row.pack(fill="x", padx=10, pady=4)
            tk.Label(row, text=key, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD, width=10, anchor="w").pack(side="left")
            val = tk.Label(row, text="—", font=FONT_STAT, fg=ACCENT2,
                           bg=CARD)
            val.pack(side="right")
            unit_lbl = tk.Label(row, text=unit, font=FONT_UNIT, fg=SUBTEXT,
                                bg=CARD)
            unit_lbl.pack(side="right")
            self._stat_labels[key] = val

        # Buttons
        self._btn_start = self._mk_btn(parent, "▶  START TEST",
                                        self._start, color=ACCENT)
        self._btn_start.pack(fill="x", padx=16, pady=(4, 4))

        self._btn_stop = self._mk_btn(parent, "■  STOP",
                                       self._stop, color=WARN)
        self._btn_stop.pack(fill="x", padx=16, pady=(0, 4))
        self._btn_stop.config(state="disabled")

        self._section_label(parent, "EXPORT")
        self._btn_img = self._mk_btn(parent, "⬇  Save Graph Image",
                                      self._export_image, color=GREEN)
        self._btn_img.pack(fill="x", padx=16, pady=(0, 4))

        self._btn_csv = self._mk_btn(parent, "⬇  Save CSV Data",
                                      self._export_csv, color=GREEN)
        self._btn_csv.pack(fill="x", padx=16, pady=(0, 10))

        self._drive_menu.bind("<<ComboboxSelected>>", self._on_drive_select)

    def _build_graph(self, parent):
        # Header
        hdr = tk.Frame(parent, bg=PANEL)
        hdr.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(hdr, text="WRITE SPEED OVER TIME",
                 font=FONT_HEADER, fg=TEXT, bg=PANEL).pack(side="left")
        self._graph_subtitle = tk.Label(hdr, text="", font=FONT_SMALL,
                                         fg=SUBTEXT, bg=PANEL)
        self._graph_subtitle.pack(side="right")

        # Progress bar
        prog_frame = tk.Frame(parent, bg=PANEL)
        prog_frame.pack(fill="x", padx=16, pady=(6, 0))
        self._prog_var = tk.DoubleVar(value=0)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("DM.Horizontal.TProgressbar",
                        troughcolor=CARD, background=ACCENT,
                        bordercolor=BORDER, lightcolor=ACCENT,
                        darkcolor=ACCENT, thickness=8)
        self._prog_bar = ttk.Progressbar(prog_frame, variable=self._prog_var,
                                          maximum=100,
                                          style="DM.Horizontal.TProgressbar")
        self._prog_bar.pack(fill="x")

        self._prog_label = tk.Label(parent, text="", font=FONT_SMALL,
                                     fg=SUBTEXT, bg=PANEL)
        self._prog_label.pack(anchor="w", padx=16, pady=(2, 6))

        # Matplotlib figure
        self._fig = Figure(figsize=(6, 4), facecolor=PANEL)
        self._ax  = self._fig.add_subplot(111)
        self._style_axes()

        self._canvas = FigureCanvasTkAgg(self._fig, master=parent)
        self._canvas.get_tk_widget().pack(fill="both", expand=True,
                                           padx=12, pady=(0, 12))
        self._canvas.draw()

    # ── Helpers ───────────────────────────────────────────────────────────

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, font=("Courier New", 8, "bold"),
                 fg=ACCENT, bg=PANEL, anchor="w").pack(
                     fill="x", padx=16, pady=(12, 2))

    def _mk_btn(self, parent, text, cmd, color=ACCENT):
        btn = tk.Button(parent, text=text, font=FONT_BTN,
                        bg=CARD, fg=color, activebackground=BORDER,
                        activeforeground=color, relief="flat",
                        bd=0, cursor="hand2", pady=7, command=cmd,
                        highlightthickness=1, highlightbackground=BORDER)
        return btn

    def _style_combobox(self):
        style = ttk.Style()
        style.configure("TCombobox",
                        fieldbackground=CARD,
                        background=CARD,
                        foreground=TEXT,
                        selectbackground=BORDER,
                        selectforeground=TEXT,
                        bordercolor=BORDER,
                        arrowcolor=ACCENT)

    def _style_axes(self):
        ax = self._ax
        ax.set_facecolor(CARD)
        ax.tick_params(colors=SUBTEXT, labelsize=8)
        ax.spines[:].set_color(BORDER)
        ax.set_xlabel("Elapsed Time (s)", color=SUBTEXT, fontsize=8,
                      fontfamily="Courier New")
        ax.set_ylabel("Write Speed (MB/s)", color=SUBTEXT, fontsize=8,
                      fontfamily="Courier New")
        ax.grid(True, color=BORDER, linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_title("Waiting for test...", color=SUBTEXT,
                     fontsize=9, fontfamily="Courier New")
        self._fig.tight_layout(pad=1.5)

    # ── Drive handling ─────────────────────────────────────────────────────

    def _refresh_drives(self):
        self._drives = get_drives()
        labels = [d[0] for d in self._drives]
        self._drive_menu["values"] = labels
        if labels:
            self._drive_menu.current(0)
            self._on_drive_select(None)

    def _on_drive_select(self, _event):
        idx = self._drive_menu.current()
        if idx < 0 or idx >= len(self._drives):
            return
        _, mp, total, free = self._drives[idx]
        fill = self._fill_var.get() / 100.0
        target = min(int(total * fill), int(free * 0.98))
        self._info_labels["Total"].config(text=_fmt_size(total))
        self._info_labels["Free"].config(text=_fmt_size(free))
        self._info_labels["Target Write"].config(text=_fmt_size(target))

    def _on_fill_change(self, val):
        v = float(val)
        self._fill_label.config(text=f"{int(v)}%")
        self._on_drive_select(None)

    # ── Benchmark control ─────────────────────────────────────────────────

    def _start(self):
        idx = self._drive_menu.current()
        if idx < 0:
            messagebox.showwarning("No Drive", "Please select a drive first.")
            return
        _, mp, total, free = self._drives[idx]
        fill = self._fill_var.get() / 100.0
        target = min(int(total * fill), int(free * 0.98))

        if target < CHUNK:
            messagebox.showerror("Insufficient Space",
                                  f"Not enough free space.\nFree: {_fmt_size(free)}")
            return

        confirm = messagebox.askyesno(
            "Confirm Test",
            f"This will write up to {_fmt_size(target)} to:\n{mp}\n\n"
            "A temporary file will be created and deleted afterward.\n\n"
            "Continue?"
        )
        if not confirm:
            return

        self._samples = []
        self._running = True
        self._btn_start.config(state="disabled")
        self._btn_stop.config(state="normal")
        self._reset_stats()
        self._reset_graph()
        self._prog_var.set(0)
        self._status_var.set(f"Writing to {mp} …")
        self._graph_subtitle.config(text=mp)

        self._worker = BenchmarkWorker(
            target_dir=mp,
            fill_fraction=fill,
            on_progress=self._cb_progress,
            on_sample=self._cb_sample,
            on_done=self._cb_done,
            on_error=self._cb_error,
        )
        self._worker.start()

    def _stop(self):
        if self._worker:
            self._worker.stop()
        self._status_var.set("Stopping…")
        self._btn_stop.config(state="disabled")

    # ── Callbacks (worker thread → GUI) ───────────────────────────────────

    def _cb_progress(self, bw, total, mb_s):
        pct = min(100.0, bw / total * 100)
        self.after(0, lambda: self._update_progress(pct, bw, total, mb_s))

    def _cb_sample(self, elapsed, mb_s):
        self._samples.append((elapsed, mb_s))
        self.after(0, lambda: self._update_graph())

    def _cb_done(self, samples, peak, avg, elapsed):
        self.after(0, lambda: self._finish(samples, peak, avg, elapsed))

    def _cb_error(self, msg):
        self.after(0, lambda: self._show_error(msg))

    # ── GUI updates ────────────────────────────────────────────────────────

    def _update_progress(self, pct, bw, total, mb_s):
        self._prog_var.set(pct)
        self._prog_label.config(
            text=f"{_fmt_size(bw)} / {_fmt_size(total)}   ({mb_s:.1f} MB/s)"
        )

    def _update_graph(self):
        if not self._samples:
            return
        xs = [s[0] for s in self._samples]
        ys = [s[1] for s in self._samples]

        ax = self._ax
        ax.cla()
        self._style_axes()

        # Fill under curve
        ax.fill_between(xs, ys, alpha=0.15, color=ACCENT)
        ax.plot(xs, ys, color=ACCENT, linewidth=1.8, marker="o",
                markersize=3.5, markerfacecolor=ACCENT2,
                markeredgewidth=0)

        # Peak annotation
        peak_idx = ys.index(max(ys))
        ax.annotate(f"Peak\n{ys[peak_idx]:.0f} MB/s",
                    xy=(xs[peak_idx], ys[peak_idx]),
                    xytext=(8, 12), textcoords="offset points",
                    color=ACCENT2, fontsize=7.5,
                    fontfamily="Courier New",
                    arrowprops=dict(arrowstyle="->",
                                   color=ACCENT2, lw=1.2))

        ax.set_title(f"Samples: {len(xs)}   |   Latest: {ys[-1]:.1f} MB/s",
                     color=TEXT, fontsize=8.5, fontfamily="Courier New")
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw_idle()

        # Live stat update
        if ys:
            self._stat_labels["Peak"].config(text=f"{max(ys):.1f}")
            avg = sum(ys) / len(ys)
            self._stat_labels["Average"].config(text=f"{avg:.1f}")

    def _finish(self, samples, peak, avg, elapsed):
        self._running = False
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")
        self._stat_labels["Peak"].config(text=f"{peak:.1f}")
        self._stat_labels["Average"].config(text=f"{avg:.1f}")
        self._stat_labels["Duration"].config(text=f"{elapsed:.1f}")
        self._prog_var.set(100)
        self._status_var.set(
            f"✓  Done  |  Peak: {peak:.1f} MB/s  |  Avg: {avg:.1f} MB/s  |  {elapsed:.1f}s"
        )
        # Finalize graph title
        ax = self._ax
        ax.set_title(
            f"COMPLETE  —  Peak {peak:.1f} MB/s  /  Avg {avg:.1f} MB/s",
            color=GREEN, fontsize=9, fontfamily="Courier New"
        )
        self._canvas.draw()

    def _show_error(self, msg):
        self._running = False
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")
        self._status_var.set(f"Error: {msg}")
        messagebox.showerror("Benchmark Error", msg)

    def _reset_stats(self):
        for lbl in self._stat_labels.values():
            lbl.config(text="—")

    def _reset_graph(self):
        ax = self._ax
        ax.cla()
        self._style_axes()
        self._canvas.draw()

    # ── Export ─────────────────────────────────────────────────────────────

    def _export_image(self):
        if not self._samples:
            messagebox.showinfo("No Data", "Run a benchmark first.")
            return
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=f"drivetest_{ts}.png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            title="Save Graph Image"
        )
        if not path:
            return
        self._fig.savefig(path, dpi=150, facecolor=PANEL,
                          bbox_inches="tight")
        self._status_var.set(f"Graph saved → {path}")

    def _export_csv(self):
        if not self._samples:
            messagebox.showinfo("No Data", "Run a benchmark first.")
            return
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"drivetest_{ts}.csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
            title="Save CSV Data"
        )
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sample", "Elapsed (s)", "Write Speed (MB/s)"])
            for i, (t, v) in enumerate(self._samples, 1):
                writer.writerow([i, f"{t:.3f}", f"{v:.2f}"])
        self._status_var.set(f"CSV saved → {path}")


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = DriveMark()
    app.mainloop()
