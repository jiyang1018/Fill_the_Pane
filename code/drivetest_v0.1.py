"""
Fill the Pane  v0.1
Sequential Write Torture Test
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
import io

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import PIL.Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ═══════════════════════════════════════════════════════════════════════════
#  Build metadata
# ═══════════════════════════════════════════════════════════════════════════
APP_NAME    = "Fill the Pane"
APP_SUBTITLE = "Sequential Write Torture Test"
APP_VERSION = "0.1"
BUILD_DT    = "2025-05-01 00:00:00"
GITHUB_URL  = "https://github.com/yourname/fillthepane"
AUTHOR      = "Your Name"
LICENSE_STR = "GNU General Public License v3.0 (GPLv3)"

# ═══════════════════════════════════════════════════════════════════════════
#  Language definitions
# ═══════════════════════════════════════════════════════════════════════════
LANGUAGES = [
    ("EN", "English"),
    ("DA", "Danish"),
    ("DE", "German"),
    ("FI", "Finnish"),
    ("FR", "French"),
    ("HU", "Hungarian"),
    ("ID", "Indonesian"),
    ("MS", "Malay"),
    ("NL", "Dutch"),
    ("NO", "Norwegian"),
    ("PL", "Polish"),
    ("PT", "Portuguese"),
    ("RO", "Romanian"),
    ("RU", "Russian"),
    ("ES", "Spanish"),
    ("SV", "Swedish"),
    ("TR", "Turkish"),
    ("UK", "Ukrainian"),
    ("VI", "Vietnamese"),
    ("AR", "Arabic"),
    ("ZH", "Chinese (Simplified)"),
    ("ZHT", "Chinese (Traditional)"),
    ("JA", "Japanese"),
    ("KO", "Korean"),
]

# Flag emoji map
FLAGS = {
    "English": "🇺🇸", "Danish": "🇩🇰", "German": "🇩🇪", "Finnish": "🇫🇮",
    "French": "🇫🇷", "Hungarian": "🇭🇺", "Indonesian": "🇮🇩", "Malay": "🇲🇾",
    "Dutch": "🇳🇱", "Norwegian": "🇳🇴", "Polish": "🇵🇱", "Portuguese": "🇵🇹",
    "Romanian": "🇷🇴", "Russian": "🇷🇺", "Spanish": "🇪🇸", "Swedish": "🇸🇪",
    "Turkish": "🇹🇷", "Ukrainian": "🇺🇦", "Vietnamese": "🇻🇳", "Arabic": "🇸🇦",
    "Chinese (Simplified)": "🇨🇳", "Chinese (Traditional)": "🇹🇼",
    "Japanese": "🇯🇵", "Korean": "🇰🇷",
}

EN = {
    "title": "Fill the Pane",
    "subtitle": "Sequential Write Torture Test",
    "select_drive": "Select Drive",
    "refresh_drives": "↺  Refresh Drives",
    "drive_info_btn": "Drive Info",
    "fill_target": "Fill Target",
    "write_up_to": "Write Up To",
    "drive_info_sec": "Drive Info",
    "total": "Total",
    "free": "Free",
    "target_write": "Target Write",
    "results": "Results",
    "peak": "Peak",
    "average": "Average",
    "duration": "Duration",
    "start_test": "▶  Start Test",
    "stop_test": "■  Stop Test",
    "save_image": "🖼  Save Graph Image",
    "save_animation": "🎬  Save Animation",
    "save_data": "📊  Save Data",
    "write_speed": "Write Speed Over Time",
    "ready": "Ready.",
    "confirm_title": "Confirm Test",
    "confirm_msg": "This will write up to {size} to:\n{path}\n\nA temporary file will be created and deleted afterward.\n\nContinue?",
    "no_drive": "No Drive",
    "no_drive_msg": "Please select a drive first.",
    "no_data": "No Data",
    "no_data_msg": "Run a benchmark first.",
    "insuff_space": "Insufficient Space",
    "insuff_msg": "Not enough free space.\nFree: {free}",
    "stopping": "Stopping…",
    "done_status": "✓  Done  |  Peak: {peak:.1f} MB/s  |  Avg: {avg:.1f} MB/s  |  {dur:.1f}s",
    "error": "Error",
    "graph_saved": "Graph saved → {path}",
    "data_saved": "Data saved → {path}",
    "anim_saved": "Animation saved → {path}",
    "export_res_title": "Export Options",
    "width_px": "Width (px):",
    "height_px": "Height (px):",
    "export_btn": "Export",
    "cancel_btn": "Cancel",
    "format_label": "Format:",
    "save_loc": "Save Location:",
    "browse": "Browse…",
    "waiting": "Waiting for Test…",
    "complete": "Complete  —  Peak {peak:.1f} MB/s  /  Avg {avg:.1f} MB/s",
    "samples_label": "Samples: {n}   |   Latest: {last:.1f} MB/s",
    "anim_unavail": "Animation export requires Pillow.\nRun: pip install Pillow",
    "export_menu": "Export",
    "language_menu": "Language",
    "about_menu": "About",
    "export_result_img": "Export Result as Image",
    "export_anim_menu": "Export Progress as Animation",
    "export_report_menu": "Export Report",
    "mb_s": "MB/s",
    "sec": "sec",
    "drive_info_title": "Drive Information",
    "mount_point": "Mount Point",
    "device": "Device",
    "file_system": "File System",
    "options": "Options",
    "total_capacity": "Total Capacity",
    "used_space": "Used Space",
    "free_space": "Free Space",
    "usage_pct": "Usage",
    "volume_name": "Volume Name",
    "serial_number": "Serial Number",
}

# Partial translations — rest fall back to English
TRANSLATIONS = {
    "English": EN,
    "German": {**EN, "subtitle": "Sequentieller Schreib-Belastungstest",
               "refresh_drives": "↺  Laufwerke Aktualisieren",
               "start_test": "▶  Test Starten", "stop_test": "■  Test Stoppen",
               "save_image": "🖼  Grafik Speichern", "save_data": "📊  Daten Speichern"},
    "French": {**EN, "subtitle": "Test de Torture d'Écriture Séquentielle",
               "refresh_drives": "↺  Actualiser les Lecteurs",
               "start_test": "▶  Démarrer le Test", "stop_test": "■  Arrêter le Test",
               "save_image": "🖼  Enregistrer l'Image", "save_data": "📊  Enregistrer les Données"},
    "Spanish": {**EN, "subtitle": "Prueba de Tortura de Escritura Secuencial",
                "refresh_drives": "↺  Actualizar Unidades",
                "start_test": "▶  Iniciar Prueba", "stop_test": "■  Detener Prueba",
                "save_image": "🖼  Guardar Imagen", "save_data": "📊  Guardar Datos"},
    "Japanese": {**EN, "subtitle": "シーケンシャル書き込み耐久テスト",
                 "start_test": "▶  テスト開始", "stop_test": "■  テスト停止",
                 "save_image": "🖼  グラフ保存", "save_data": "📊  データ保存"},
    "Chinese (Simplified)": {**EN, "subtitle": "顺序写入压力测试",
                              "start_test": "▶  开始测试", "stop_test": "■  停止测试",
                              "save_image": "🖼  保存图表", "save_data": "📊  保存数据"},
    "Korean": {**EN, "subtitle": "순차 쓰기 고문 테스트",
               "start_test": "▶  테스트 시작", "stop_test": "■  테스트 중지",
               "save_image": "🖼  그래프 저장", "save_data": "📊  데이터 저장"},
}
# All other languages default to English
for _code, _name in LANGUAGES:
    if _name not in TRANSLATIONS:
        TRANSLATIONS[_name] = EN


def T(lang, key):
    return TRANSLATIONS.get(lang, EN).get(key, EN.get(key, key))


# ═══════════════════════════════════════════════════════════════════════════
#  Drive helpers
# ═══════════════════════════════════════════════════════════════════════════

def _fmt_size(n):
    if n is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def get_drives():
    drives = []
    if HAS_PSUTIL:
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                label = f"💾  {part.device}  ({part.mountpoint})  —  {_fmt_size(usage.total)}"
                drives.append((label, part.mountpoint, usage.total, usage.free, part))
            except Exception:
                pass
    else:
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            mp = f"{letter}:\\"
            if os.path.exists(mp):
                try:
                    total, used, free = shutil.disk_usage(mp)
                    label = f"💾  {mp}  —  {_fmt_size(total)}"
                    drives.append((label, mp, total, free, None))
                except Exception:
                    pass
    return drives


def get_drive_info(mountpoint, part_obj, lang="English"):
    info = {}
    try:
        total, used, free = shutil.disk_usage(mountpoint)
        info[T(lang, "total_capacity")] = _fmt_size(total)
        info[T(lang, "used_space")]     = _fmt_size(used)
        info[T(lang, "free_space")]     = _fmt_size(free)
        info[T(lang, "usage_pct")]      = f"{used/total*100:.1f}%"
    except Exception:
        pass
    if HAS_PSUTIL and part_obj:
        info[T(lang, "mount_point")] = part_obj.mountpoint
        info[T(lang, "device")]      = part_obj.device
        info[T(lang, "file_system")] = part_obj.fstype or "Unknown"
        opts = part_obj.opts or ""
        info[T(lang, "options")]     = opts if opts else "—"
    if platform.system() == "Windows":
        try:
            import ctypes
            vol  = ctypes.create_unicode_buffer(261)
            ser  = ctypes.c_ulong()
            fsn  = ctypes.create_unicode_buffer(261)
            ctypes.windll.kernel32.GetVolumeInformationW(
                mountpoint, vol, 261, ctypes.byref(ser), None, None, fsn, 261
            )
            if vol.value:
                info[T(lang, "volume_name")] = vol.value
            info[T(lang, "serial_number")] = f"{ser.value:08X}"
        except Exception:
            pass
    return info


# ═══════════════════════════════════════════════════════════════════════════
#  Benchmark worker
# ═══════════════════════════════════════════════════════════════════════════

CHUNK            = 4 * 1024 * 1024
MEASURE_INTERVAL = 0.5


class BenchmarkWorker(threading.Thread):
    def __init__(self, target_dir, fill_fraction,
                 on_progress, on_sample, on_done, on_error):
        super().__init__(daemon=True)
        self.target_dir    = target_dir
        self.fill_fraction = fill_fraction
        self.on_progress   = on_progress
        self.on_sample     = on_sample
        self.on_done       = on_done
        self.on_error      = on_error
        self._stop         = threading.Event()
        self.target_bytes  = 0

    def stop(self):
        self._stop.set()

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

        tb = int(total * self.fill_fraction)
        tb = min(tb, int(free * 0.98))
        self.target_bytes = tb

        if tb < CHUNK:
            self.on_error(
                f"Not enough free space.\nFree: {_fmt_size(free)}, needed: {_fmt_size(CHUNK)}"
            )
            return

        tmp  = os.path.join(self.target_dir, "_fillthepane_.tmp")
        data = os.urandom(CHUNK)

        samples        = []
        bytes_written  = 0
        t0             = time.perf_counter()
        t_interval     = t0
        interval_bytes = 0

        try:
            with open(tmp, "wb", buffering=0) as f:
                while bytes_written < tb:
                    if self._stop.is_set():
                        break
                    remaining  = tb - bytes_written
                    write_size = min(CHUNK, remaining)
                    f.write(data[:write_size])
                    f.flush()
                    os.fsync(f.fileno())
                    bytes_written  += write_size
                    interval_bytes += write_size

                    now = time.perf_counter()
                    if now - t_interval >= MEASURE_INTERVAL:
                        mb_s    = (interval_bytes / (now - t_interval)) / (1024 * 1024)
                        elapsed = now - t0
                        samples.append((elapsed, mb_s, bytes_written))
                        self.on_sample(elapsed, mb_s, bytes_written, tb)
                        self.on_progress(bytes_written, tb, mb_s)
                        t_interval     = now
                        interval_bytes = 0
        except OSError:
            pass
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass

        if not samples:
            self.on_error("No data collected. Drive may be too fast or too small.")
            return

        total_elapsed = time.perf_counter() - t0
        peak = max(s[1] for s in samples)
        avg  = sum(s[1] for s in samples) / len(samples)
        self.on_done(samples, peak, avg, total_elapsed)


# ═══════════════════════════════════════════════════════════════════════════
#  Theme constants
# ═══════════════════════════════════════════════════════════════════════════

BG      = "#0d0f14"
PANEL   = "#13161e"
CARD    = "#1a1e2a"
ACCENT  = "#00d4ff"
ACCENT2 = "#ff6b35"
TEXT    = "#e8eaf0"
SUBTEXT = "#7a8099"
GREEN   = "#39d353"
RED_C   = "#e05555"
WARN    = "#f0c040"
BORDER  = "#252a38"

FN          = "Courier New"
FONT_TITLE  = (FN, 19, "bold")
FONT_SMALL  = (FN, 9)
FONT_STAT   = (FN, 13, "bold")
FONT_UNIT   = (FN, 8)
FONT_BTN    = (FN, 10, "bold")
FONT_HEADER = (FN, 10, "bold")
FONT_MENU   = (FN, 10)
FONT_SEC    = (FN, 8, "bold")


# ═══════════════════════════════════════════════════════════════════════════
#  Export dialog
# ═══════════════════════════════════════════════════════════════════════════

class ExportDialog(tk.Toplevel):
    def __init__(self, parent, title, formats, default_name, lang="English"):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.result    = None
        self._lang     = lang
        self._formats  = formats
        self._defname  = default_name
        self._path_var = tk.StringVar()
        self._fmt_var  = tk.StringVar(value=formats[0])
        self._w_var    = tk.IntVar(value=1920)
        self._h_var    = tk.IntVar(value=1080)
        self._build()
        self._center(parent)

    def _center(self, p):
        self.update_idletasks()
        x = p.winfo_rootx() + p.winfo_width()  // 2 - 210
        y = p.winfo_rooty() + p.winfo_height() // 2 - 140
        self.geometry(f"420x290+{x}+{y}")

    def _row(self, parent, label):
        tk.Label(parent, text=label, font=FONT_SMALL, fg=SUBTEXT,
                 bg=BG, anchor="w").pack(fill="x", padx=20, pady=(10, 2))

    def _build(self):
        tk.Label(self, text=T(self._lang, "export_res_title"),
                 font=FONT_HEADER, fg=ACCENT, bg=BG).pack(pady=(14, 4))

        res = tk.Frame(self, bg=BG)
        res.pack(fill="x", padx=20)
        tk.Label(res, text=T(self._lang, "width_px"),
                 font=FONT_SMALL, fg=SUBTEXT, bg=BG).pack(side="left")
        tk.Entry(res, textvariable=self._w_var, font=FONT_SMALL,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 bd=4, width=7).pack(side="left", padx=(4, 14))
        tk.Label(res, text=T(self._lang, "height_px"),
                 font=FONT_SMALL, fg=SUBTEXT, bg=BG).pack(side="left")
        tk.Entry(res, textvariable=self._h_var, font=FONT_SMALL,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 bd=4, width=7).pack(side="left", padx=4)

        self._row(self, T(self._lang, "format_label"))
        fmts = tk.Frame(self, bg=BG)
        fmts.pack(fill="x", padx=20)
        for fmt in self._formats:
            tk.Radiobutton(fmts, text=fmt, variable=self._fmt_var, value=fmt,
                           font=FONT_SMALL, fg=TEXT, bg=BG, selectcolor=CARD,
                           activebackground=BG, activeforeground=ACCENT
                           ).pack(side="left", padx=6)

        self._row(self, T(self._lang, "save_loc"))
        pr = tk.Frame(self, bg=BG)
        pr.pack(fill="x", padx=20)
        tk.Entry(pr, textvariable=self._path_var, font=FONT_SMALL,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 bd=4).pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Button(pr, text=T(self._lang, "browse"), font=FONT_SMALL,
                  bg=CARD, fg=ACCENT, relief="flat",
                  command=self._browse).pack(side="right")

        br = tk.Frame(self, bg=BG)
        br.pack(pady=14)
        tk.Button(br, text=T(self._lang, "export_btn"), font=FONT_BTN,
                  bg=GREEN, fg=BG, relief="flat", padx=14, pady=5,
                  command=self._ok).pack(side="left", padx=8)
        tk.Button(br, text=T(self._lang, "cancel_btn"), font=FONT_BTN,
                  bg=CARD, fg=TEXT, relief="flat", padx=14, pady=5,
                  command=self.destroy).pack(side="left", padx=8)

    def _browse(self):
        fmt = self._fmt_var.get().lower()
        ext = f".{fmt}"
        ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        p   = filedialog.asksaveasfilename(
            defaultextension=ext,
            initialfile=f"{self._defname}_{ts}{ext}",
            filetypes=[(fmt.upper(), f"*{ext}"), ("All Files", "*.*")]
        )
        if p:
            self._path_var.set(p)

    def _ok(self):
        if not self._path_var.get():
            self._browse()
            if not self._path_var.get():
                return
        self.result = {
            "width":  self._w_var.get(),
            "height": self._h_var.get(),
            "format": self._fmt_var.get(),
            "path":   self._path_var.get(),
        }
        self.destroy()


# ═══════════════════════════════════════════════════════════════════════════
#  Drive Info dialog
# ═══════════════════════════════════════════════════════════════════════════

class DriveInfoDialog(tk.Toplevel):
    def __init__(self, parent, info_dict, lang="English"):
        super().__init__(parent)
        self.title(T(lang, "drive_info_title"))
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text=T(lang, "drive_info_title"),
                 font=FONT_HEADER, fg=ACCENT, bg=BG).pack(pady=(16, 8))

        frm = tk.Frame(self, bg=CARD, highlightthickness=1,
                       highlightbackground=BORDER)
        frm.pack(fill="both", padx=20, pady=(0, 8))
        for k, v in info_dict.items():
            r = tk.Frame(frm, bg=CARD)
            r.pack(fill="x", padx=12, pady=3)
            tk.Label(r, text=k, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD, width=18, anchor="w").pack(side="left")
            tk.Label(r, text=str(v), font=FONT_SMALL, fg=TEXT,
                     bg=CARD, anchor="e").pack(side="right")

        tk.Button(self, text="Close", font=FONT_BTN, bg=CARD, fg=TEXT,
                  relief="flat", padx=18, pady=5,
                  command=self.destroy).pack(pady=10)
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width()  // 2 - self.winfo_width()  // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")


# ═══════════════════════════════════════════════════════════════════════════
#  About dialog
# ═══════════════════════════════════════════════════════════════════════════

class AboutDialog(tk.Toplevel):
    def __init__(self, parent, lang="English"):
        super().__init__(parent)
        self.title(f"About {APP_NAME}")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text=APP_NAME, font=(FN, 17, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=(20, 2))
        tk.Label(self, text=APP_SUBTITLE, font=FONT_SMALL,
                 fg=SUBTEXT, bg=BG).pack()
        tk.Label(self, text=f"Version {APP_VERSION}", font=FONT_SMALL,
                 fg=TEXT, bg=BG).pack(pady=(8, 2))
        tk.Label(self, text=f"Build: {BUILD_DT}", font=FONT_SMALL,
                 fg=SUBTEXT, bg=BG).pack()

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=12)

        tk.Label(self, text=f"Author: {AUTHOR}", font=FONT_SMALL,
                 fg=TEXT, bg=BG).pack()
        tk.Label(self, text=LICENSE_STR, font=FONT_SMALL,
                 fg=SUBTEXT, bg=BG).pack(pady=(4, 0))

        lnk = tk.Label(self, text=GITHUB_URL, font=FONT_SMALL,
                       fg=ACCENT, bg=BG, cursor="hand2")
        lnk.pack(pady=(4, 14))
        lnk.bind("<Button-1>", lambda e: __import__("webbrowser").open(GITHUB_URL))

        tk.Button(self, text="Close", font=FONT_BTN, bg=CARD, fg=TEXT,
                  relief="flat", padx=18, pady=5,
                  command=self.destroy).pack(pady=(0, 16))
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width()  // 2 - self.winfo_width()  // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")


# ═══════════════════════════════════════════════════════════════════════════
#  Main Application
# ═══════════════════════════════════════════════════════════════════════════

class FillThePane(tk.Tk):

    def __init__(self):
        super().__init__()
        self._lang          = "English"
        self._worker        = None
        self._samples       = []   # (elapsed, mb_s, bytes_written)
        self._running       = False
        self._fill_var      = tk.DoubleVar(value=90.0)
        self._drive_var     = tk.StringVar()
        self._drives        = []
        self._target_bytes  = 0
        self._frame_snaps   = []   # PIL Images for GIF animation
        self._vline         = None
        self._hover_ann     = None

        self.title(f"{APP_NAME}  —  {APP_SUBTITLE}")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(960, 660)
        self._build_ui()
        self._refresh_drives()
        self.after(200, self._center_window)

    def _(self, key):
        return T(self._lang, key)

    # ─── Window ───────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 1100, 720
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    # ─── Build UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_menubar()

        # Title bar
        tb = tk.Frame(self, bg=BG, pady=7)
        tb.pack(fill="x", padx=18)
        tk.Label(tb, text="⬡ " + self._("title"),
                 font=FONT_TITLE, fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(tb, text="  —  " + self._("subtitle"),
                 font=(FN, 10), fg=SUBTEXT, bg=BG).pack(side="left", pady=3)

        # Body
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=PANEL, width=290,
                        highlightthickness=1, highlightbackground=BORDER)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        left.pack_propagate(False)
        self._build_left(left)

        right = tk.Frame(body, bg=PANEL,
                         highlightthickness=1, highlightbackground=BORDER)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_graph(right)

        # Status bar
        self._status_var = tk.StringVar(value=self._("ready"))
        tk.Label(self, textvariable=self._status_var, font=FONT_SMALL,
                 fg=SUBTEXT, bg=BG, anchor="w").pack(fill="x", padx=20, pady=(0, 4))

    def _build_menubar(self):
        mb = tk.Menu(self, bg=PANEL, fg=TEXT, activebackground=CARD,
                     activeforeground=ACCENT, relief="flat", font=FONT_MENU)
        self.config(menu=mb)

        # Export menu
        em = tk.Menu(mb, tearoff=0, bg=PANEL, fg=TEXT, activebackground=CARD,
                     activeforeground=ACCENT, font=FONT_MENU)
        mb.add_cascade(label=self._("export_menu"), menu=em)
        em.add_command(label=self._("export_result_img"),
                       command=self._do_export_image)
        em.add_command(label=self._("export_anim_menu"),
                       command=self._do_export_animation)
        em.add_command(label=self._("export_report_menu"),
                       command=self._do_export_report)

        # Language menu
        lm = tk.Menu(mb, tearoff=0, bg=PANEL, fg=TEXT, activebackground=CARD,
                     activeforeground=ACCENT, font=FONT_MENU)
        mb.add_cascade(label=self._("language_menu"), menu=lm)
        for _code, name in LANGUAGES:
            flag = FLAGS.get(name, "")
            lm.add_command(
                label=f"{flag}  {name}",
                command=lambda n=name: self._set_language(n)
            )

        mb.add_command(label=self._("about_menu"), command=self._show_about)

    def _build_left(self, p):
        def sec(text):
            tk.Label(p, text=text.upper(), font=FONT_SEC,
                     fg=ACCENT, bg=PANEL, anchor="w").pack(
                         fill="x", padx=14, pady=(10, 2))

        def btn(text, cmd, color=ACCENT):
            b = tk.Button(p, text=text, font=FONT_BTN, bg=CARD, fg=color,
                          activebackground=BORDER, activeforeground=color,
                          relief="flat", bd=0, cursor="hand2", pady=6,
                          command=cmd, highlightthickness=1,
                          highlightbackground=BORDER)
            return b

        # Drive selection
        sec(self._("select_drive"))
        dr = tk.Frame(p, bg=PANEL)
        dr.pack(fill="x", padx=14, pady=(0, 3))
        tk.Label(dr, text="💾", font=(FN, 12), bg=PANEL,
                 fg=ACCENT).pack(side="left", padx=(0, 4))
        self._drive_menu = ttk.Combobox(dr, textvariable=self._drive_var,
                                         state="readonly", font=FONT_SMALL)
        self._drive_menu.pack(side="left", fill="x", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                        foreground=TEXT, selectbackground=BORDER,
                        selectforeground=TEXT, bordercolor=BORDER, arrowcolor=ACCENT)
        style.configure("DM.Horizontal.TProgressbar",
                        troughcolor=CARD, background=ACCENT,
                        bordercolor=BORDER, lightcolor=ACCENT,
                        darkcolor=ACCENT, thickness=20)

        btn(self._("refresh_drives"), self._refresh_drives, SUBTEXT).pack(
            fill="x", padx=14, pady=(2, 2))
        btn(self._("drive_info_btn"), self._show_drive_info, ACCENT).pack(
            fill="x", padx=14, pady=(0, 8))

        # Fill target
        sec(self._("fill_target"))
        fr = tk.Frame(p, bg=PANEL)
        fr.pack(fill="x", padx=14, pady=(0, 2))
        tk.Label(fr, text=self._("write_up_to"), font=FONT_SMALL,
                 fg=SUBTEXT, bg=PANEL).pack(side="left")
        self._fill_label = tk.Label(fr, text="90%", font=FONT_STAT,
                                     fg=ACCENT, bg=PANEL, width=5)
        self._fill_label.pack(side="right")
        tk.Scale(p, from_=10, to=90, orient="horizontal",
                 variable=self._fill_var, bg=PANEL, fg=TEXT,
                 troughcolor=CARD, activebackground=ACCENT,
                 highlightthickness=0, bd=0, sliderlength=18,
                 command=self._on_fill_change, font=FONT_SMALL
                 ).pack(fill="x", padx=14, pady=(0, 8))

        # Drive info card
        sec(self._("drive_info_sec"))
        ifrm = tk.Frame(p, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        ifrm.pack(fill="x", padx=14, pady=(0, 8))
        self._info_labels = {}
        for key in (self._("total"), self._("free"), self._("target_write")):
            r = tk.Frame(ifrm, bg=CARD)
            r.pack(fill="x", padx=10, pady=3)
            tk.Label(r, text=key, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD, width=13, anchor="w").pack(side="left")
            lbl = tk.Label(r, text="—", font=FONT_SMALL, fg=TEXT,
                           bg=CARD, anchor="e")
            lbl.pack(side="right")
            self._info_labels[key] = lbl

        # Results card
        sec(self._("results"))
        sfrm = tk.Frame(p, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        sfrm.pack(fill="x", padx=14, pady=(0, 8))
        self._stat_labels = {}
        for key, unit in ((self._("peak"),     self._("mb_s")),
                          (self._("average"),  self._("mb_s")),
                          (self._("duration"), self._("sec"))):
            r = tk.Frame(sfrm, bg=CARD)
            r.pack(fill="x", padx=10, pady=4)
            tk.Label(r, text=key, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD, width=10, anchor="w").pack(side="left")
            tk.Label(r, text=unit, font=FONT_UNIT, fg=SUBTEXT,
                     bg=CARD).pack(side="right")
            val = tk.Label(r, text="—", font=FONT_STAT,
                           fg=ACCENT2, bg=CARD)
            val.pack(side="right")
            self._stat_labels[key] = val

        # Action buttons
        self._btn_start = btn(self._("start_test"), self._start, GREEN)
        self._btn_start.pack(fill="x", padx=14, pady=(4, 3))
        self._btn_stop  = btn(self._("stop_test"),  self._stop,  RED_C)
        self._btn_stop.pack(fill="x", padx=14, pady=(0, 8))
        self._btn_stop.config(state="disabled")

        # Export buttons (same behavior as menu items)
        btn(self._("save_image"),     self._do_export_image,     ACCENT).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("save_animation"), self._do_export_animation, ACCENT).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("save_data"),      self._do_export_report,    ACCENT).pack(fill="x", padx=14, pady=(0, 10))

        self._drive_menu.bind("<<ComboboxSelected>>", self._on_drive_select)

    def _build_graph(self, p):
        hdr = tk.Frame(p, bg=PANEL)
        hdr.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(hdr, text=self._("write_speed").upper(),
                 font=FONT_HEADER, fg=TEXT, bg=PANEL).pack(side="left")
        self._graph_subtitle = tk.Label(hdr, text="", font=FONT_SMALL,
                                         fg=SUBTEXT, bg=PANEL)
        self._graph_subtitle.pack(side="right")

        # Progress bar container (for overlay label)
        prog_outer = tk.Frame(p, bg=PANEL)
        prog_outer.pack(fill="x", padx=14, pady=(6, 0))
        self._prog_var = tk.DoubleVar(value=0)
        self._prog_bar = ttk.Progressbar(
            prog_outer, variable=self._prog_var, maximum=100,
            style="DM.Horizontal.TProgressbar"
        )
        self._prog_bar.pack(fill="x")

        # Percentage label floating on top of bar
        self._pct_lbl = tk.Label(prog_outer, text="0%",
                                  font=(FN, 8, "bold"), fg="white", bg=PANEL)
        self._pct_lbl.place(relx=0.5, rely=0.5, anchor="center")
        self._prog_bar.bind("<Configure>",
            lambda e: self._pct_lbl.place(in_=self._prog_bar,
                                           relx=0.5, rely=0.5, anchor="center"))

        self._prog_detail = tk.Label(p, text="", font=FONT_SMALL,
                                      fg=SUBTEXT, bg=PANEL)
        self._prog_detail.pack(anchor="w", padx=14, pady=(2, 4))

        # Matplotlib figure
        self._fig = Figure(figsize=(6, 4), facecolor=PANEL)
        self._ax  = self._fig.add_subplot(111)
        self._style_axes()
        self._canvas = FigureCanvasTkAgg(self._fig, master=p)
        self._canvas.get_tk_widget().pack(fill="both", expand=True,
                                           padx=10, pady=(0, 10))
        self._canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        self._canvas.mpl_connect("axes_leave_event",    self._on_axes_leave)
        self._canvas.draw()

    # ─── Helpers ──────────────────────────────────────────────────────────

    def _style_axes(self):
        ax = self._ax
        ax.set_facecolor(CARD)
        ax.tick_params(colors=SUBTEXT, labelsize=8)
        ax.spines[:].set_color(BORDER)
        ax.set_xlabel("Elapsed Time (s)", color=SUBTEXT, fontsize=8, fontfamily=FN)
        ax.set_ylabel("Write Speed (MB/s)", color=SUBTEXT, fontsize=8, fontfamily=FN)
        ax.grid(True, color=BORDER, linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_title(self._("waiting"), color=SUBTEXT, fontsize=9, fontfamily=FN)
        self._fig.tight_layout(pad=1.5)

    # ─── Language ─────────────────────────────────────────────────────────

    def _set_language(self, lang):
        self._lang = lang
        messagebox.showinfo("Language / 语言 / 言語",
                            f"Language set to: {lang}\n\nRestart to apply all UI strings.")

    # ─── Drive handling ───────────────────────────────────────────────────

    def _refresh_drives(self):
        self._drives = get_drives()
        self._drive_menu["values"] = [d[0] for d in self._drives]
        if self._drives:
            self._drive_menu.current(0)
            self._on_drive_select(None)

    def _on_drive_select(self, _e):
        idx = self._drive_menu.current()
        if idx < 0 or idx >= len(self._drives):
            return
        _, mp, total, free, _ = self._drives[idx]
        fill   = self._fill_var.get() / 100.0
        target = min(int(total * fill), int(free * 0.98))
        for key, val in (
            (self._("total"),        _fmt_size(total)),
            (self._("free"),         _fmt_size(free)),
            (self._("target_write"), _fmt_size(target)),
        ):
            if key in self._info_labels:
                self._info_labels[key].config(text=val)

    def _on_fill_change(self, val):
        self._fill_label.config(text=f"{int(float(val))}%")
        self._on_drive_select(None)

    def _show_drive_info(self):
        idx = self._drive_menu.current()
        if idx < 0:
            messagebox.showwarning(self._("no_drive"), self._("no_drive_msg"))
            return
        _, mp, total, free, part_obj = self._drives[idx]
        info = get_drive_info(mp, part_obj, self._lang)
        DriveInfoDialog(self, info, self._lang)

    # ─── Benchmark ────────────────────────────────────────────────────────

    def _start(self):
        idx = self._drive_menu.current()
        if idx < 0:
            messagebox.showwarning(self._("no_drive"), self._("no_drive_msg"))
            return
        _, mp, total, free, _ = self._drives[idx]
        fill   = self._fill_var.get() / 100.0
        target = min(int(total * fill), int(free * 0.98))
        if target < CHUNK:
            messagebox.showerror(
                self._("insuff_space"),
                self._("insuff_msg").format(free=_fmt_size(free))
            )
            return
        if not messagebox.askyesno(
            self._("confirm_title"),
            self._("confirm_msg").format(size=_fmt_size(target), path=mp)
        ):
            return

        self._samples      = []
        self._frame_snaps  = []
        self._running      = True
        self._target_bytes = target
        self._btn_start.config(state="disabled")
        self._btn_stop.config(state="normal")
        for lbl in self._stat_labels.values():
            lbl.config(text="—")
        self._ax.cla()
        self._style_axes()
        self._canvas.draw()
        self._prog_var.set(0)
        self._pct_lbl.config(text="0%")
        self._status_var.set(f"Writing to {mp} …")
        self._graph_subtitle.config(text=mp)

        self._worker = BenchmarkWorker(
            target_dir=mp, fill_fraction=fill,
            on_progress=self._cb_progress, on_sample=self._cb_sample,
            on_done=self._cb_done, on_error=self._cb_error,
        )
        self._worker.start()

    def _stop(self):
        if self._worker:
            self._worker.stop()
        self._status_var.set(self._("stopping"))
        self._btn_stop.config(state="disabled")

    # ─── Worker callbacks ─────────────────────────────────────────────────

    def _cb_progress(self, bw, total, mb_s):
        pct = min(100.0, bw / total * 100)
        self.after(0, lambda: self._update_progress(pct, bw, total, mb_s))

    def _cb_sample(self, elapsed, mb_s, bw, tb):
        self._samples.append((elapsed, mb_s, bw))
        self.after(0, lambda: self._update_graph(capture=True))

    def _cb_done(self, samples, peak, avg, elapsed):
        self.after(0, lambda: self._finish(samples, peak, avg, elapsed))

    def _cb_error(self, msg):
        self.after(0, lambda: self._show_error(msg))

    # ─── GUI updates ──────────────────────────────────────────────────────

    def _update_progress(self, pct, bw, total, mb_s):
        self._prog_var.set(pct)
        self._pct_lbl.config(text=f"{pct:.0f}%")
        self._pct_lbl.place(in_=self._prog_bar, relx=0.5, rely=0.5, anchor="center")
        self._prog_detail.config(
            text=f"{_fmt_size(bw)} / {_fmt_size(total)}   ({mb_s:.1f} MB/s)"
        )

    def _update_graph(self, capture=False):
        if not self._samples:
            return
        xs = [s[0] for s in self._samples]
        ys = [s[1] for s in self._samples]

        ax = self._ax
        ax.cla()
        self._style_axes()
        ax.fill_between(xs, ys, alpha=0.15, color=ACCENT)
        ax.plot(xs, ys, color=ACCENT, linewidth=1.8, marker="o",
                markersize=3.5, markerfacecolor=ACCENT2, markeredgewidth=0)

        pi = ys.index(max(ys))
        ax.annotate(f"Peak\n{ys[pi]:.0f} MB/s",
                    xy=(xs[pi], ys[pi]),
                    xytext=(8, 12), textcoords="offset points",
                    color=ACCENT2, fontsize=7.5, fontfamily=FN,
                    arrowprops=dict(arrowstyle="->", color=ACCENT2, lw=1.2))

        ax.set_title(self._("samples_label").format(n=len(xs), last=ys[-1]),
                     color=TEXT, fontsize=8.5, fontfamily=FN)
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw_idle()

        pk_lbl = self._("peak")
        av_lbl = self._("average")
        if pk_lbl in self._stat_labels:
            self._stat_labels[pk_lbl].config(text=f"{max(ys):.1f}")
        if av_lbl in self._stat_labels:
            self._stat_labels[av_lbl].config(text=f"{sum(ys)/len(ys):.1f}")

        if capture and HAS_PIL:
            buf = io.BytesIO()
            self._fig.savefig(buf, format="png", facecolor=PANEL, dpi=72)
            buf.seek(0)
            img = PIL.Image.open(buf).copy()
            self._frame_snaps.append(img)
            buf.close()

    def _finish(self, samples, peak, avg, elapsed):
        self._running = False
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")
        for key, val in (
            (self._("peak"),     f"{peak:.1f}"),
            (self._("average"),  f"{avg:.1f}"),
            (self._("duration"), f"{elapsed:.1f}"),
        ):
            if key in self._stat_labels:
                self._stat_labels[key].config(text=val)
        self._prog_var.set(100)
        self._pct_lbl.config(text="100%")
        self._pct_lbl.place(in_=self._prog_bar, relx=0.5, rely=0.5, anchor="center")
        self._status_var.set(
            self._("done_status").format(peak=peak, avg=avg, dur=elapsed)
        )
        self._ax.set_title(
            self._("complete").format(peak=peak, avg=avg),
            color=GREEN, fontsize=9, fontfamily=FN
        )
        self._canvas.draw()

    def _show_error(self, msg):
        self._running = False
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")
        self._status_var.set(f"{self._('error')}: {msg}")
        messagebox.showerror("Benchmark Error", msg)

    # ─── Mouse crosshair ─────────────────────────────────────────────────

    def _on_mouse_move(self, event):
        if not self._samples or event.inaxes != self._ax:
            return
        xs = [s[0] for s in self._samples]
        ys = [s[1] for s in self._samples]
        bs = [s[2] for s in self._samples]
        xd = event.xdata
        if xd is None:
            return
        idx = min(range(len(xs)), key=lambda i: abs(xs[i] - xd))
        tb  = self._target_bytes if self._target_bytes > 0 else 1

        if self._vline:
            try:
                self._vline.remove()
            except Exception:
                pass
        if self._hover_ann:
            try:
                self._hover_ann.remove()
            except Exception:
                pass

        self._vline = self._ax.axvline(x=xs[idx], color=WARN,
                                        linewidth=0.9, linestyle="--", alpha=0.85)
        self._hover_ann = self._ax.annotate(
            f"{_fmt_size(bs[idx])}\n{bs[idx]/tb*100:.1f}% full",
            xy=(xs[idx], ys[idx]),
            xytext=(10, -30), textcoords="offset points",
            fontsize=7.5, fontfamily=FN, color=WARN,
            bbox=dict(boxstyle="round,pad=0.3", fc=CARD, ec=WARN, lw=0.8, alpha=0.9)
        )
        self._canvas.draw_idle()

    def _on_axes_leave(self, event):
        changed = False
        for attr in ("_vline", "_hover_ann"):
            obj = getattr(self, attr)
            if obj:
                try:
                    obj.remove()
                except Exception:
                    pass
                setattr(self, attr, None)
                changed = True
        if changed:
            self._canvas.draw_idle()

    # ─── Export actions (shared by menu + buttons) ────────────────────────

    def _guard_data(self):
        if not self._samples:
            messagebox.showinfo(self._("no_data"), self._("no_data_msg"))
            return False
        return True

    def _do_export_image(self):
        if not self._guard_data():
            return
        dlg = ExportDialog(self, self._("export_result_img"),
                           ["PNG", "JPG", "GIF"], "fillthepane_graph", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r    = dlg.result
        fmt  = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"

        # Render at requested pixel size
        dpi  = 100
        orig = self._fig.get_size_inches()
        self._fig.set_size_inches(r["width"] / dpi, r["height"] / dpi)
        self._fig.savefig(path, dpi=dpi, facecolor=PANEL, bbox_inches="tight",
                          format="jpeg" if fmt == "jpg" else fmt)
        self._fig.set_size_inches(*orig)
        self._canvas.draw_idle()
        self._status_var.set(self._("graph_saved").format(path=path))

    def _do_export_animation(self):
        if not self._guard_data():
            return
        if not HAS_PIL:
            messagebox.showwarning("Pillow Required", self._("anim_unavail"))
            return
        if len(self._frame_snaps) < 2:
            messagebox.showinfo("Not Enough Frames",
                                "Complete or run a test to capture animation frames.")
            return
        dlg = ExportDialog(self, self._("export_anim_menu"),
                           ["GIF", "MP4"], "fillthepane_anim", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r    = dlg.result
        fmt  = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        tw, th = r["width"], r["height"]

        if fmt == "gif":
            frames = [f.resize((tw, th), PIL.Image.LANCZOS)
                      for f in self._frame_snaps]
            frames[0].save(path, save_all=True, append_images=frames[1:],
                           loop=0, duration=120, optimize=False)
            self._status_var.set(self._("anim_saved").format(path=path))
        else:
            try:
                import matplotlib.animation as manim
                fd = [(s[0], s[1]) for s in self._samples]
                fig2, ax2 = plt.subplots(facecolor=PANEL)
                ax2.set_facecolor(CARD)
                ax2.tick_params(colors=SUBTEXT)
                ax2.spines[:].set_color(BORDER)
                line, = ax2.plot([], [], color=ACCENT, linewidth=1.8)
                ax2.set_xlim(0, max(s[0] for s in fd) * 1.05)
                ax2.set_ylim(0, max(s[1] for s in fd) * 1.2)
                ax2.set_xlabel("Elapsed (s)", color=SUBTEXT, fontsize=8)
                ax2.set_ylabel("MB/s", color=SUBTEXT, fontsize=8)
                fig2.tight_layout()

                def _anim(i):
                    line.set_data([fd[j][0] for j in range(i+1)],
                                  [fd[j][1] for j in range(i+1)])
                    return line,

                ani = manim.FuncAnimation(fig2, _anim, frames=len(fd),
                                          interval=100, blit=True)
                dpi = max(72, min(tw, th) // 4)
                ani.save(path, writer=manim.FFMpegWriter(fps=10, codec="libx265"),
                         dpi=dpi)
                plt.close(fig2)
                self._status_var.set(self._("anim_saved").format(path=path))
            except Exception as e:
                messagebox.showerror("MP4 Failed",
                    f"Could not export MP4.\nEnsure ffmpeg is installed.\n\n{e}")

    def _do_export_report(self):
        if not self._guard_data():
            return
        dlg = ExportDialog(self, self._("export_report_menu"),
                           ["CSV", "XLS", "NUMBERS"],
                           "fillthepane_data", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r    = dlg.result
        fmt  = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        tb   = self._target_bytes if self._target_bytes > 0 else 1
        rows = [(i+1, s[0], s[1], s[2], s[2]/tb*100)
                for i, s in enumerate(self._samples)]
        hdrs = ["Sample", "Elapsed (s)", "Write Speed (MB/s)",
                "Bytes Written", "Capacity %"]

        if fmt == "csv":
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdrs)
                for row in rows:
                    w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                row[3], f"{row[4]:.2f}"])

        elif fmt == "xls":
            try:
                import xlwt
                wb = xlwt.Workbook()
                ws = wb.add_sheet("Benchmark")
                for ci, h in enumerate(hdrs):
                    ws.write(0, ci, h)
                for ri, row in enumerate(rows, 1):
                    ws.write(ri, 0, row[0])
                    ws.write(ri, 1, round(row[1], 3))
                    ws.write(ri, 2, round(row[2], 2))
                    ws.write(ri, 3, row[3])
                    ws.write(ri, 4, round(row[4], 2))
                wb.save(path)
            except ImportError:
                with open(path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(hdrs)
                    for row in rows:
                        w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                    row[3], f"{row[4]:.2f}"])
                messagebox.showinfo(
                    "Note", "xlwt not installed — saved as CSV.\nInstall xlwt for true XLS."
                )

        else:  # numbers
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdrs)
                for row in rows:
                    w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                row[3], f"{row[4]:.2f}"])
            messagebox.showinfo(
                "Note",
                "Saved as CSV — open with Apple Numbers or rename to .csv.\n"
                "Full .numbers format requires macOS Numbers."
            )

        self._status_var.set(self._("data_saved").format(path=path))

    def _show_about(self):
        AboutDialog(self, self._lang)


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = FillThePane()
    app.mainloop()
