"""
Fill the Pane  v0.2
Sequential Write Torture Test
https://github.com/jiyang1018/Fill_the_Pane
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
import io
import configparser
import math

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
APP_NAME     = "Fill the Pane"
APP_SUBTITLE = "Sequential Write Torture Test"
APP_VERSION  = "0.2"
BUILD_DT     = "2025-05-01 00:00:00"
GITHUB_URL   = "https://github.com/jiyang1018/Fill_the_Pane"
AUTHOR       = "Yang Ji"
LICENSE_STR  = "GNU General Public License v3.0 (GPLv3)"

# ═══════════════════════════════════════════════════════════════════════════
#  Settings
# ═══════════════════════════════════════════════════════════════════════════

def _settings_path():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "settings.ini")


def load_settings():
    cfg = configparser.ConfigParser()
    cfg.read(_settings_path(), encoding="utf-8")
    lang  = cfg.get("App", "language", fallback="English")
    theme = cfg.get("App", "theme",    fallback="dark")
    return lang, theme


def save_settings(lang, theme):
    cfg = configparser.ConfigParser()
    cfg["App"] = {"language": lang, "theme": theme}
    try:
        with open(_settings_path(), "w", encoding="utf-8") as f:
            cfg.write(f)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
#  Theme system
# ═══════════════════════════════════════════════════════════════════════════

DARK_THEME = {
    "BG":        "#0d0f14",
    "PANEL":     "#13161e",
    "CARD":      "#1a1e2a",
    "ACCENT":    "#00d4ff",
    "ACCENT2":   "#ff6b35",
    "TEXT":      "#e8eaf0",
    "SUBTEXT":   "#7a8099",
    "GREEN":     "#39d353",
    "ORANGE":    "#ff9a3c",
    "RED_C":     "#e05555",
    "WARN":      "#f0c040",
    "BORDER":    "#252a38",
    "RED_VAL":   "#ff4444",
    "RED_BORDER":"#cc2222",
    # light mode overrides for text — dark theme uses light text
    "TEXT_FIXED": "#e8eaf0",   # always light in dark mode
    "SEC_LBL":   "#00d4ff",    # section label color — accent in dark mode
}

LIGHT_THEME = {
    "BG":        "#f0f2f5",
    "PANEL":     "#ffffff",
    "CARD":      "#e8ecf2",
    "ACCENT":    "#0077cc",
    "ACCENT2":   "#e05000",
    "TEXT":      "#000000",    # black in light mode
    "SUBTEXT":   "#000000",    # black in light mode
    "GREEN":     "#1a8a34",
    "ORANGE":    "#c06000",
    "RED_C":     "#cc2222",
    "WARN":      "#b07000",
    "BORDER":    "#c8cdd8",
    "RED_VAL":   "#cc0000",
    "RED_BORDER":"#cc0000",
    "TEXT_FIXED": "#000000",
    "SEC_LBL":   "#000000",    # section label color — black in light mode
}

TH = dict(DARK_THEME)

def th(key):
    return TH[key]

# ═══════════════════════════════════════════════════════════════════════════
#  Font
# ═══════════════════════════════════════════════════════════════════════════

FN = "Segoe UI Variable" if platform.system() == "Windows" else "Inter"

def FONT_TITLE():  return (FN, 24, "bold")
def FONT_SMALL():  return (FN, 10)
def FONT_STAT():   return (FN, 15, "bold")
def FONT_UNIT():   return (FN, 10)
def FONT_BTN():    return (FN, 12, "bold")
def FONT_HEADER(): return (FN, 12, "bold")
def FONT_MENU():   return (FN, 10)
def FONT_SEC():    return (FN, 10, "bold")

# ═══════════════════════════════════════════════════════════════════════════
#  Language definitions
# ═══════════════════════════════════════════════════════════════════════════

LANGUAGES = [
    ("ENG", "English",               "English",           "🇺🇸"),
    ("DAN", "Danish",                "Dansk",             "🇩🇰"),
    ("DEU", "German",                "Deutsch",           "🇩🇪"),
    ("FIN", "Finnish",               "Suomi",             "🇫🇮"),
    ("FRA", "French",                "Français",          "🇫🇷"),
    ("HUN", "Hungarian",             "Magyar",            "🇭🇺"),
    ("IND", "Indonesian",            "Bahasa Indonesia",  "🇮🇩"),
    ("MSA", "Malay",                 "Bahasa Melayu",     "🇲🇾"),
    ("NLD", "Dutch",                 "Nederlands",        "🇳🇱"),
    ("NOR", "Norwegian",             "Norsk",             "🇳🇴"),
    ("POL", "Polish",                "Polski",            "🇵🇱"),
    ("POR", "Portuguese",            "Português",         "🇵🇹"),
    ("RON", "Romanian",              "Română",            "🇷🇴"),
    ("RUS", "Russian",               "Русский",           "🇷🇺"),
    ("SPA", "Spanish",               "Español",           "🇪🇸"),
    ("SWE", "Swedish",               "Svenska",           "🇸🇪"),
    ("TUR", "Turkish",               "Türkçe",            "🇹🇷"),
    ("UKR", "Ukrainian",             "Українська",        "🇺🇦"),
    ("VIE", "Vietnamese",            "Tiếng Việt",        "🇻🇳"),
    ("ARA", "Arabic",                "العربية",           "🇸🇦"),
    ("ZHO", "Chinese (Simplified)",  "简体中文",           "🇨🇳"),
    ("ZHT", "Chinese (Traditional)", "繁體中文",           "🇹🇼"),
    ("JPN", "Japanese",              "日本語",            "🇯🇵"),
    ("KOR", "Korean",                "한국어",            "🇰🇷"),
]

EN = {
    "title":              "Fill the Pane",
    "subtitle":           "Sequential Write Torture Test",
    "select_drive":       "Select Drive",
    "refresh_drives":     "↺  Refresh Drives",
    "fill_target":        "Fill Target",
    "write_up_to":        "Write Up To",
    "drive_info_sec":     "Drive Info",
    "total":              "Total",
    "free":               "Free",
    "target_write":       "Target Write",
    "results":            "Results",
    "peak":               "Peak",
    "average":            "Average",
    "duration":           "Duration",
    "start_test":         "▶  Start Test",
    "stop_test":          "■  Stop Test",
    "save_image":         "🖼  Save Graph Image",
    "save_animation":     "🎬  Save Animation",
    "save_data":          "📊  Save Data",
    "load_data":          "📂  Load Data",
    "save_infographic":   "Infographic for Web",
    "write_speed":        "Write Speed Over Time",
    "ready":              "Ready.",
    "confirm_title":      "Confirm Test",
    "confirm_msg":        "This will write up to {size} to:\n{path}\n\nA temporary file will be created and deleted afterward.\n\nContinue?",
    "no_drive":           "No Drive",
    "no_drive_msg":       "Please select a drive first.",
    "no_data":            "No Data",
    "no_data_msg":        "Run a benchmark first.",
    "insuff_space":       "Insufficient Space",
    "insuff_msg":         "Not enough free space.\nFree: {free}",
    "stopping":           "Stopping…",
    "done_status":        "✓  Done  |  Peak: {peak:.1f} MB/s  |  Avg: {avg:.1f} MB/s  |  {dur:.1f}s",
    "error":              "Error",
    "graph_saved":        "Graph Saved → {path}",
    "data_saved":         "Data Saved → {path}",
    "anim_saved":         "Animation Saved → {path}",
    "data_loaded":        "Data Loaded → {path}",
    "export_res_title":   "Export Options",
    "width_px":           "Width (px):",
    "height_px":          "Height (px):",
    "export_btn":         "Export",
    "cancel_btn":         "Cancel",
    "format_label":       "Format:",
    "save_loc":           "Save Location:",
    "browse":             "Browse…",
    "waiting":            "Waiting for Test…",
    "complete":           "Complete  —  Peak {peak:.1f} MB/s  /  Avg {avg:.1f} MB/s",
    "samples_label":      "Samples: {n}   |   Latest: {last:.1f} MB/s",
    "anim_unavail":       "Animation Export Requires Pillow.\nRun: pip install Pillow",
    "language_menu":      "Language",
    "theme_menu":         "Theme",
    "dark_mode":          "Dark Mode",
    "light_mode":         "Light Mode",
    "about_menu":         "About",
    "about_program":      "About This Program",
    "export_result_img":  "Export Result as Image",
    "export_anim_menu":   "Export Progress as Animation",
    "export_report_menu": "Export Report",
    "mb_s":               "MB/s",
    "sec":                "sec",
    "drive_info_title":   "Drive Information",
    "mount_point":        "Mount Point",
    "device":             "Device",
    "file_system":        "File System",
    "options":            "Options",
    "total_capacity":     "Total Capacity",
    "used_space":         "Used Space",
    "free_space":         "Free Space",
    "usage_pct":          "Usage",
    "volume_name":        "Volume Name",
    "serial_number":      "Serial Number",
    "capacity_axis":      "Drive Capacity Written",
    "exceed_warn":        "Fill target exceeds free space.",
    "load_csv_title":     "Load CSV Data",
    "load_csv_invalid":   "Invalid CSV file. Expected columns: Elapsed (s), Write Speed (MB/s), Bytes Written.",
}

TRANSLATIONS = {
    "English": EN,
    "German": {**EN,
        "subtitle":       "Sequentieller Schreib-Belastungstest",
        "refresh_drives": "↺  Laufwerke Aktualisieren",
        "start_test":     "▶  Test Starten",
        "stop_test":      "■  Test Stoppen",
        "save_image":     "🖼  Grafik Speichern",
        "save_data":      "📊  Daten Speichern",
        "load_data":      "📂  Daten Laden",
        "capacity_axis":  "Geschriebene Laufwerkskapazität",
    },
    "French": {**EN,
        "subtitle":       "Test de Torture d'Écriture Séquentielle",
        "refresh_drives": "↺  Actualiser les Lecteurs",
        "start_test":     "▶  Démarrer le Test",
        "stop_test":      "■  Arrêter le Test",
        "save_image":     "🖼  Enregistrer l'Image",
        "save_data":      "📊  Enregistrer les Données",
        "load_data":      "📂  Charger les Données",
        "capacity_axis":  "Capacité du Lecteur Écrite",
    },
    "Spanish": {**EN,
        "subtitle":       "Prueba de Tortura de Escritura Secuencial",
        "refresh_drives": "↺  Actualizar Unidades",
        "start_test":     "▶  Iniciar Prueba",
        "stop_test":      "■  Detener Prueba",
        "save_image":     "🖼  Guardar Imagen",
        "save_data":      "📊  Guardar Datos",
        "load_data":      "📂  Cargar Datos",
        "capacity_axis":  "Capacidad del Disco Escrita",
    },
    "Japanese": {**EN,
        "subtitle":       "シーケンシャル書き込み耐久テスト",
        "start_test":     "▶  テスト開始",
        "stop_test":      "■  テスト停止",
        "save_image":     "🖼  グラフ保存",
        "save_data":      "📊  データ保存",
        "load_data":      "📂  データ読込",
        "capacity_axis":  "書き込み済み容量",
    },
    "Chinese (Simplified)": {**EN,
        "subtitle":       "顺序写入压力测试",
        "start_test":     "▶  开始测试",
        "stop_test":      "■  停止测试",
        "save_image":     "🖼  保存图表",
        "save_data":      "📊  保存数据",
        "load_data":      "📂  加载数据",
        "capacity_axis":  "已写入容量",
    },
    "Korean": {**EN,
        "subtitle":       "순차 쓰기 고문 테스트",
        "start_test":     "▶  테스트 시작",
        "stop_test":      "■  테스트 중지",
        "save_image":     "🖼  그래프 저장",
        "save_data":      "📊  데이터 저장",
        "load_data":      "📂  데이터 불러오기",
        "capacity_axis":  "드라이브 용량 기록",
    },
}
for _iso, _eng, _native, _flag in LANGUAGES:
    if _eng not in TRANSLATIONS:
        TRANSLATIONS[_eng] = EN


def Tr(lang, key):
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


def _bytes_to_gb(n):
    return n / (1024 ** 3)


def get_drives():
    drives = []
    if HAS_PSUTIL:
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                label = f"{part.device}  ({part.mountpoint})  —  {_fmt_size(usage.total)}"
                drives.append((label, part.mountpoint, usage.total, usage.free, part))
            except Exception:
                pass
    else:
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            mp = f"{letter}:\\"
            if os.path.exists(mp):
                try:
                    total, used, free = shutil.disk_usage(mp)
                    label = f"{mp}  —  {_fmt_size(total)}"
                    drives.append((label, mp, total, free, None))
                except Exception:
                    pass
    return drives


# ═══════════════════════════════════════════════════════════════════════════
#  Benchmark worker  — CrystalDiskMark-comparable sequential write
#  Sequential 1 MB, Queue Depth = 8, Threads = 1  (CDM SEQ1M Q8T1)
# ═══════════════════════════════════════════════════════════════════════════

CHUNK            = 1 * 1024 * 1024    # 1 MB per request — CDM SEQ1M
QUEUE_DEPTH      = 8                   # 8 outstanding writes — CDM Q8
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
        import concurrent.futures
        try:
            total, used, free = shutil.disk_usage(self.target_dir)
        except Exception as e:
            self.on_error(f"Cannot read disk usage: {e}")
            return

        tb = int(total * self.fill_fraction)
        tb = min(tb, int(free * 0.98))
        self.target_bytes = tb

        min_needed = CHUNK * QUEUE_DEPTH
        if tb < min_needed:
            self.on_error(
                f"Not enough free space.\nFree: {_fmt_size(free)}, needed: {_fmt_size(min_needed)}"
            )
            return

        tmp  = os.path.join(self.target_dir, "_fillthepane_.tmp")
        # Pre-allocate 1 MB random buffer in RAM — shared by all queue slots
        data = os.urandom(CHUNK)

        # Pre-create file at full target size so threads can seek independently
        try:
            with open(tmp, "wb") as f:
                f.seek(tb - 1)
                f.write(b"\x00")
        except OSError as e:
            self.on_error(f"Cannot pre-allocate file: {e}")
            return

        samples        = []
        bytes_written  = 0
        t0             = time.perf_counter()
        t_interval     = t0
        interval_bytes = 0
        pos_lock       = threading.Lock()
        bw_lock        = threading.Lock()
        next_offset    = [0]

        def _write_slot(fd):
            with pos_lock:
                offset = next_offset[0]
                remaining = tb - offset
                if remaining <= 0 or self._stop.is_set():
                    return 0
                write_size = min(CHUNK, remaining)
                next_offset[0] += write_size
            fd.seek(offset)
            fd.write(data[:write_size])
            return write_size

        try:
            with open(tmp, "r+b", buffering=0) as fd:
                with concurrent.futures.ThreadPoolExecutor(max_workers=QUEUE_DEPTH) as pool:
                    futures = {pool.submit(_write_slot, fd) for _ in range(QUEUE_DEPTH)}

                    while futures and not self._stop.is_set():
                        done, futures = concurrent.futures.wait(
                            futures,
                            timeout=MEASURE_INTERVAL,
                            return_when=concurrent.futures.FIRST_COMPLETED
                        )
                        chunk_bytes = 0
                        for fut in done:
                            try:
                                n = fut.result()
                            except Exception:
                                n = 0
                            chunk_bytes += n
                            if next_offset[0] < tb and not self._stop.is_set():
                                futures.add(pool.submit(_write_slot, fd))

                        bytes_written  += chunk_bytes
                        interval_bytes += chunk_bytes

                        now = time.perf_counter()
                        if now - t_interval >= MEASURE_INTERVAL:
                            elapsed = now - t0
                            dt = now - t_interval
                            mb_s = (interval_bytes / dt) / (1024 * 1024) if dt > 0 else 0
                            if mb_s > 0:
                                samples.append((elapsed, mb_s, bytes_written))
                                self.on_sample(elapsed, mb_s, bytes_written, tb)
                                self.on_progress(bytes_written, tb, mb_s)
                            t_interval     = now
                            interval_bytes = 0

                try:
                    os.fsync(fd.fileno())
                except Exception:
                    pass

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
#  Export dialog
# ═══════════════════════════════════════════════════════════════════════════

class ExportDialog(tk.Toplevel):
    def __init__(self, parent, title, formats, default_name, lang="English"):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=th("BG"))
        self.resizable(False, False)
        self.grab_set()
        self.result   = None
        self._lang    = lang
        self._formats = formats
        self._defname = default_name
        self._path_var = tk.StringVar()
        self._fmt_var  = tk.StringVar(value=formats[0])
        self._w_var    = tk.IntVar(value=1920)
        self._h_var    = tk.IntVar(value=1080)
        self._build()
        self._center(parent)

    def _center(self, p):
        self.update_idletasks()
        x = p.winfo_rootx() + p.winfo_width()  // 2 - 210
        y = p.winfo_rooty() + p.winfo_height() // 2 - 145
        self.geometry(f"420x295+{x}+{y}")

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, font=FONT_SMALL(), fg=th("SUBTEXT"),
                 bg=th("BG"), anchor="w").pack(fill="x", padx=20, pady=(10, 2))

    def _build(self):
        tk.Label(self, text=Tr(self._lang, "export_res_title"),
                 font=FONT_HEADER(), fg=th("ACCENT"), bg=th("BG")).pack(pady=(14, 4))

        res = tk.Frame(self, bg=th("BG"))
        res.pack(fill="x", padx=20)
        tk.Label(res, text=Tr(self._lang, "width_px"), font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG")).pack(side="left")
        tk.Entry(res, textvariable=self._w_var, font=FONT_SMALL(),
                 bg=th("CARD"), fg=th("TEXT"), insertbackground=th("TEXT"),
                 relief="flat", bd=4, width=7).pack(side="left", padx=(4, 14))
        tk.Label(res, text=Tr(self._lang, "height_px"), font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG")).pack(side="left")
        tk.Entry(res, textvariable=self._h_var, font=FONT_SMALL(),
                 bg=th("CARD"), fg=th("TEXT"), insertbackground=th("TEXT"),
                 relief="flat", bd=4, width=7).pack(side="left", padx=4)

        self._lbl(self, Tr(self._lang, "format_label"))
        fmts = tk.Frame(self, bg=th("BG"))
        fmts.pack(fill="x", padx=20)
        for fmt in self._formats:
            tk.Radiobutton(fmts, text=fmt, variable=self._fmt_var, value=fmt,
                           font=FONT_SMALL(), fg=th("TEXT_FIXED"), bg=th("BG"),
                           selectcolor=th("CARD"), activebackground=th("BG"),
                           activeforeground=th("ACCENT")).pack(side="left", padx=6)

        self._lbl(self, Tr(self._lang, "save_loc"))
        pr = tk.Frame(self, bg=th("BG"))
        pr.pack(fill="x", padx=20)
        tk.Entry(pr, textvariable=self._path_var, font=FONT_SMALL(),
                 bg=th("CARD"), fg=th("TEXT"), insertbackground=th("TEXT"),
                 relief="flat", bd=4).pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Button(pr, text=Tr(self._lang, "browse"), font=FONT_SMALL(),
                  bg=th("CARD"), fg=th("ACCENT"), relief="flat",
                  command=self._browse).pack(side="right")

        br = tk.Frame(self, bg=th("BG"))
        br.pack(pady=14)
        tk.Button(br, text=Tr(self._lang, "export_btn"), font=FONT_BTN(),
                  bg=th("GREEN"), fg="#ffffff", relief="flat", padx=14, pady=5,
                  command=self._ok).pack(side="left", padx=8)
        tk.Button(br, text=Tr(self._lang, "cancel_btn"), font=FONT_BTN(),
                  bg=th("CARD"), fg=th("TEXT_FIXED"), relief="flat", padx=14, pady=5,
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
#  About dialog
# ═══════════════════════════════════════════════════════════════════════════

class AboutDialog(tk.Toplevel):
    def __init__(self, parent, lang="English"):
        super().__init__(parent)
        self.title(Tr(lang, "about_program"))
        self.configure(bg=th("BG"))
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text=APP_NAME, font=(FN, 18, "bold"),
                 fg=th("ACCENT"), bg=th("BG")).pack(pady=(20, 2))
        tk.Label(self, text=APP_SUBTITLE, font=FONT_SMALL(),
                 fg=th("TEXT_FIXED"), bg=th("BG")).pack()
        tk.Label(self, text=f"Version {APP_VERSION}", font=FONT_SMALL(),
                 fg=th("TEXT_FIXED"), bg=th("BG")).pack(pady=(8, 0))

        tk.Frame(self, bg=th("BORDER"), height=1).pack(fill="x", padx=20, pady=12)

        tk.Label(self, text=f"Author: {AUTHOR}", font=FONT_SMALL(),
                 fg=th("TEXT_FIXED"), bg=th("BG")).pack()
        tk.Label(self, text=LICENSE_STR, font=FONT_SMALL(),
                 fg=th("TEXT_FIXED"), bg=th("BG")).pack(pady=(4, 0))

        lnk = tk.Label(self, text=GITHUB_URL, font=FONT_SMALL(),
                       fg=th("ACCENT"), bg=th("BG"), cursor="hand2")
        lnk.pack(pady=(4, 14))
        lnk.bind("<Button-1>", lambda e: __import__("webbrowser").open(GITHUB_URL))

        tk.Button(self, text="Close", font=FONT_BTN(), bg=th("CARD"),
                  fg=th("TEXT_FIXED"), relief="flat", padx=18, pady=5,
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

        self._lang, _theme_mode = load_settings()
        TH.clear()
        TH.update(DARK_THEME if _theme_mode == "dark" else LIGHT_THEME)
        self._theme_mode = _theme_mode

        self._worker       = None
        self._samples      = []
        self._running      = False
        self._fill_var     = tk.DoubleVar(value=90.0)
        self._fill_min     = 5     # minimum fill %, recomputed on drive select
        self._drive_var    = tk.StringVar()
        self._drives       = []
        self._target_bytes = 0
        self._drive_total  = 0
        self._frame_snaps  = []
        self._vline        = None
        self._hover_ann    = None

        self.title(f"{APP_NAME} v{APP_VERSION}  —  {APP_SUBTITLE}")
        self.configure(bg=th("BG"))
        self.resizable(True, True)
        self.minsize(960, 600)
        self._build_ui()
        self._refresh_drives()
        self.after(200, self._center_window)

    def _(self, key):
        return Tr(self._lang, key)

    def _center_window(self):
        self.update_idletasks()
        w, h = 1160, 720
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    # ─── Build UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_menubar()

        tb = tk.Frame(self, bg=th("BG"), pady=7)
        tb.pack(fill="x", padx=18)
        tk.Label(tb, text="⬡ " + self._("title"),
                 font=FONT_TITLE(), fg=th("ACCENT"), bg=th("BG")).pack(side="left")
        tk.Label(tb, text=f"  v{APP_VERSION}  —  " + self._("subtitle"),
                 font=FONT_SMALL(), fg=th("SUBTEXT"), bg=th("BG")).pack(side="left", pady=3)

        body = tk.Frame(self, bg=th("BG"))
        body.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._left_frame = tk.Frame(body, bg=th("PANEL"), width=295,
                        highlightthickness=1, highlightbackground=th("BORDER"))
        self._left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        self._left_frame.pack_propagate(False)
        self._build_left(self._left_frame)

        self._right_frame = tk.Frame(body, bg=th("PANEL"),
                         highlightthickness=1, highlightbackground=th("BORDER"))
        self._right_frame.grid(row=0, column=1, sticky="nsew")
        self._build_graph(self._right_frame)

        self._status_var = tk.StringVar(value=self._("ready"))
        self._status_lbl = tk.Label(self, textvariable=self._status_var,
                                     font=FONT_SMALL(), fg=th("SUBTEXT"),
                                     bg=th("BG"), anchor="w")
        self._status_lbl.pack(fill="x", padx=20, pady=(0, 4))

    def _build_menubar(self):
        mb = tk.Menu(self, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     relief="flat", font=FONT_MENU())
        self.config(menu=mb)
        self._menubar = mb

        # Language menu — national flag emoji only (no ISO code text)
        lm = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("language_menu"), menu=lm)
        for iso, eng, native, flag in LANGUAGES:
            lm.add_command(
                label=f"{flag}  {native}",
                command=lambda n=eng: self._set_language(n)
            )

        # Theme menu
        tm = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("theme_menu"), menu=tm)
        tm.add_command(label=self._("dark_mode"),  command=lambda: self._set_theme("dark"))
        tm.add_command(label=self._("light_mode"), command=lambda: self._set_theme("light"))

        # About menu → About This Program
        am = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("about_menu"), menu=am)
        am.add_command(label=self._("about_program"), command=self._show_about)

    def _build_left(self, p):
        def sec(text):
            tk.Label(p, text=text, font=FONT_SEC(),
                     fg=th("SEC_LBL"), bg=th("PANEL"), anchor="w").pack(
                         fill="x", padx=14, pady=(10, 2))

        def btn(text, cmd, color):
            return tk.Button(p, text=text, font=FONT_BTN(), bg=th("CARD"), fg=color,
                             activebackground=th("BORDER"), activeforeground=color,
                             relief="flat", bd=0, cursor="hand2", pady=6,
                             anchor="w", padx=12, justify="left",
                             command=cmd, highlightthickness=1,
                             highlightbackground=th("BORDER"))

        # ── Select Drive  (icon moved to Save Data button)
        sec("Select Drive")
        dr = tk.Frame(p, bg=th("PANEL"))
        dr.pack(fill="x", padx=14, pady=(0, 3))
        self._drive_menu = ttk.Combobox(dr, textvariable=self._drive_var,
                                         state="readonly", font=FONT_SMALL())
        self._drive_menu.pack(side="left", fill="x", expand=True)
        self._style_ttk()

        btn(self._("refresh_drives"), self._refresh_drives, th("SUBTEXT")).pack(
            fill="x", padx=14, pady=(2, 8))

        # ── Fill Target
        sec("Fill Target")
        fr = tk.Frame(p, bg=th("PANEL"))
        fr.pack(fill="x", padx=14, pady=(0, 2))
        tk.Label(fr, text="Write Up To", font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="left")
        self._fill_label = tk.Label(fr, text="90%", font=FONT_STAT(),
                                     fg=th("ACCENT"), bg=th("PANEL"), width=5)
        self._fill_label.pack(side="right")
        # Slider visual range is always 0–100; draggable range clamped to [_fill_min, 90]
        self._fill_slider = tk.Scale(p, from_=0, to=100, orient="horizontal",
                 variable=self._fill_var, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                 troughcolor=th("CARD"), activebackground=th("ACCENT"),
                 highlightthickness=0, bd=0, sliderlength=18, showvalue=0,
                 command=self._on_fill_change, font=FONT_SMALL())
        self._fill_slider.pack(fill="x", padx=14, pady=(0, 2))
        tick_row = tk.Frame(p, bg=th("PANEL"))
        tick_row.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(tick_row, text="0%", font=(FN, 8), fg=th("SUBTEXT"),
                 bg=th("PANEL")).pack(side="left")
        tk.Label(tick_row, text="100%", font=(FN, 8), fg=th("SUBTEXT"),
                 bg=th("PANEL")).pack(side="right")

        # ── Drive Info card
        sec("Drive Info")
        self._info_frame = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                                     highlightbackground=th("BORDER"))
        self._info_frame.pack(fill="x", padx=14, pady=(0, 8))
        self._info_labels = {}
        for key in ("Total", "Free", "Target Write"):
            r = tk.Frame(self._info_frame, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=3)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=13, anchor="w").pack(side="left")
            lbl = tk.Label(r, text="—", font=FONT_SMALL(), fg=th("TEXT_FIXED"),
                           bg=th("CARD"), anchor="e")
            lbl.pack(side="right")
            self._info_labels[key] = lbl

        # ── Results card
        sec("Results")
        sfrm = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                        highlightbackground=th("BORDER"))
        sfrm.pack(fill="x", padx=14, pady=(0, 8))
        self._stat_labels = {}
        # Peak = green, Average = orange, Duration = black/light
        stat_colors = {"Peak": th("GREEN"), "Average": th("ORANGE"), "Duration": th("TEXT_FIXED")}
        for key, unit in (("Peak", "MB/s"), ("Average", "MB/s"), ("Duration", "sec")):
            r = tk.Frame(sfrm, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=4)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=10, anchor="w").pack(side="left")
            tk.Label(r, text=unit, font=FONT_UNIT(), fg=th("SUBTEXT"),
                     bg=th("CARD")).pack(side="right")
            val = tk.Label(r, text="—", font=FONT_STAT(),
                           fg=stat_colors[key], bg=th("CARD"))
            val.pack(side="right")
            self._stat_labels[key] = val

        # ── Error label (sits above Start Test)
        self._error_var = tk.StringVar(value="")
        self._error_lbl = tk.Label(p, textvariable=self._error_var,
                                    font=FONT_SMALL(), fg=th("RED_VAL"),
                                    bg=th("PANEL"), anchor="w", wraplength=260)
        self._error_lbl.pack(fill="x", padx=14, pady=(4, 0))

        # ── Action buttons
        self._btn_start = btn(self._("start_test"), self._start, th("GREEN"))
        self._btn_start.pack(fill="x", padx=14, pady=(2, 3))
        self._btn_stop  = btn(self._("stop_test"),  self._stop,  th("RED_C"))
        self._btn_stop.pack(fill="x", padx=14, pady=(0, 8))
        self._btn_stop.config(state="disabled")

        # ── Export/Load buttons  (💾 icon on Save Data)
        btn(self._("save_image"),     self._do_export_image,     th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("save_animation"), self._do_export_animation, th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("💾  " + self._("save_data"),  self._do_export_report,    th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("load_data"),      self._do_load_data,        th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("🌐  " + self._("save_infographic"), self._do_export_infographic, th("ACCENT")).pack(fill="x", padx=14, pady=(0, 10))

        self._drive_menu.bind("<<ComboboxSelected>>", self._on_drive_select)

    def _build_graph(self, p):
        hdr = tk.Frame(p, bg=th("PANEL"))
        hdr.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(hdr, text="Write Speed Over Time",
                 font=FONT_HEADER(), fg=th("TEXT_FIXED"), bg=th("PANEL")).pack(side="left")
        self._graph_subtitle = tk.Label(hdr, text="", font=FONT_SMALL(),
                                         fg=th("SUBTEXT"), bg=th("PANEL"))
        self._graph_subtitle.pack(side="right")

        self._write_status_var = tk.StringVar(value="")
        tk.Label(p, textvariable=self._write_status_var,
                 font=FONT_SMALL(), fg=th("SUBTEXT"),
                 bg=th("PANEL"), anchor="w").pack(fill="x", padx=14, pady=(4, 2))

        self._graph_container = tk.Frame(p, bg=th("PANEL"))
        self._graph_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._fig = Figure(facecolor=th("PANEL"))
        self._fig.set_size_inches(16, 9)
        self._ax  = self._fig.add_subplot(111)
        self._style_axes()

        self._canvas = FigureCanvasTkAgg(self._fig, master=self._graph_container)
        widget = self._canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Configure>", self._on_graph_resize)
        self._canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        self._canvas.mpl_connect("axes_leave_event",    self._on_axes_leave)
        self._canvas.draw()

    def _on_graph_resize(self, event):
        w_px, h_px = event.width, event.height
        if w_px < 10 or h_px < 10:
            return
        dpi  = self._fig.get_dpi()
        w_in = w_px / dpi
        h_in = w_in * 9 / 16
        if h_px / dpi < h_in:
            h_in = h_px / dpi
            w_in = h_in * 16 / 9
        self._fig.set_size_inches(w_in, h_in, forward=False)
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw_idle()

    # ─── Styling ──────────────────────────────────────────────────────────

    def _style_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=th("CARD"), background=th("CARD"),
                        foreground=th("TEXT_FIXED"), selectbackground=th("BORDER"),
                        selectforeground=th("TEXT_FIXED"), bordercolor=th("BORDER"),
                        arrowcolor=th("ACCENT"))

    def _style_axes(self):
        ax = self._ax
        ax.set_facecolor(th("CARD"))
        ax.tick_params(colors=th("SUBTEXT"), labelsize=9)
        ax.spines[:].set_color(th("BORDER"))
        x_label = self._("capacity_axis")
        if self._drive_total > 0:
            total_gb = _bytes_to_gb(self._drive_total)
            if total_gb >= 1:
                x_label += f"  (GB, max {total_gb:.1f} GB)"
            else:
                x_label += f"  (MB, max {self._drive_total/(1024**2):.0f} MB)"
        ax.set_xlabel(x_label, color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        ax.set_ylabel("Write Speed (MB/s)", color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        ax.grid(True, color=th("BORDER"), linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_title(self._("waiting"), color=th("SUBTEXT"), fontsize=10, fontfamily=FN)
        self._fig.set_facecolor(th("PANEL"))
        self._fig.tight_layout(pad=1.5)

    # ─── Theme ────────────────────────────────────────────────────────────

    def _set_theme(self, mode):
        if mode == self._theme_mode:
            return
        self._theme_mode = mode
        TH.clear()
        TH.update(DARK_THEME if mode == "dark" else LIGHT_THEME)
        save_settings(self._lang, mode)
        for widget in self.winfo_children():
            widget.destroy()
        self._vline = None
        self._hover_ann = None
        self._build_ui()
        self._refresh_drives()
        if self._samples:
            self._update_graph()

    # ─── Language ─────────────────────────────────────────────────────────

    def _set_language(self, lang):
        self._lang = lang
        save_settings(lang, self._theme_mode)
        messagebox.showinfo(
            "Language / 语言 / 言語",
            f"Language set to: {lang}\n\nRestart to apply all UI strings."
        )

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
        self._drive_total = total

        # Compute dynamic minimum: max(5%, used% + 5%)
        used = total - free
        used_pct = (used / total * 100) if total > 0 else 0
        self._fill_min = max(5, min(math.ceil(used_pct + 5), 89))  # never >= 90

        # Clamp current slider value into [_fill_min, 90]
        current = self._fill_var.get()
        if current < self._fill_min:
            self._fill_var.set(self._fill_min)
        elif current > 90:
            self._fill_var.set(90)

        fill    = self._fill_var.get() / 100.0
        target  = int(total * fill)
        exceeds = target > free

        # Info card values — red on exceed
        self._info_labels["Total"].config(
            text=_fmt_size(total), fg=th("TEXT_FIXED"))
        self._info_labels["Free"].config(
            text=_fmt_size(free),
            fg=th("RED_VAL") if exceeds else th("TEXT_FIXED"))
        self._info_labels["Target Write"].config(
            text=_fmt_size(target),
            fg=th("RED_VAL") if exceeds else th("TEXT_FIXED"))

        # Info card border — red on exceed
        self._info_frame.config(
            highlightbackground=th("RED_BORDER") if exceeds else th("BORDER"))

        if exceeds:
            self._btn_start.config(state="disabled", fg=th("SUBTEXT"))
            self._error_var.set(self._("exceed_warn"))
            self._status_var.set(self._("exceed_warn"))
        else:
            self._btn_start.config(state="normal", fg=th("GREEN"))
            self._error_var.set("")
            self._status_var.set(self._("ready"))

        self._ax.cla()
        self._style_axes()
        self._canvas.draw_idle()

    def _on_fill_change(self, val):
        v = int(float(val))
        # Clamp to [_fill_min, 90]
        if v < self._fill_min:
            self._fill_var.set(self._fill_min)
            v = self._fill_min
        elif v > 90:
            self._fill_var.set(90)
            v = 90
        self._fill_label.config(text=f"{v}%")
        self._on_drive_select(None)

    # ─── Benchmark ────────────────────────────────────────────────────────

    def _start(self):
        idx = self._drive_menu.current()
        if idx < 0:
            messagebox.showwarning(self._("no_drive"), self._("no_drive_msg"))
            return
        _, mp, total, free, _ = self._drives[idx]
        self._drive_total = total
        fill   = self._fill_var.get() / 100.0
        target = min(int(total * fill), int(free * 0.98))
        if target < CHUNK:
            messagebox.showerror(self._("insuff_space"),
                                  self._("insuff_msg").format(free=_fmt_size(free)))
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
        self._error_var.set("")
        for lbl in self._stat_labels.values():
            lbl.config(text="—")
        self._ax.cla()
        self._style_axes()
        self._canvas.draw()
        self._write_status_var.set("")
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
        self.after(0, lambda: self._update_write_status(pct, bw, total, mb_s))

    def _cb_sample(self, elapsed, mb_s, bw, tb):
        self._samples.append((elapsed, mb_s, bw))
        self.after(0, lambda: self._update_graph(capture=True))

    def _cb_done(self, samples, peak, avg, elapsed):
        self.after(0, lambda: self._finish(samples, peak, avg, elapsed))

    def _cb_error(self, msg):
        self.after(0, lambda: self._show_error(msg))

    # ─── GUI updates ──────────────────────────────────────────────────────

    def _update_write_status(self, pct, bw, total, mb_s):
        self._write_status_var.set(
            f"{_fmt_size(bw)} / {_fmt_size(total)}  ({pct:.1f}%)   {mb_s:.1f} MB/s"
        )

    def _x_val(self, bytes_written):
        if self._drive_total <= 0:
            return _bytes_to_gb(bytes_written)
        total_gb = _bytes_to_gb(self._drive_total)
        return _bytes_to_gb(bytes_written) if total_gb >= 1 else bytes_written / (1024**2)

    def _x_label(self):
        if self._drive_total <= 0:
            return self._("capacity_axis") + " (GB)"
        unit = "GB" if _bytes_to_gb(self._drive_total) >= 1 else "MB"
        return f"{self._('capacity_axis')} ({unit})"

    def _x_max(self):
        if self._drive_total <= 0:
            return None
        total_gb = _bytes_to_gb(self._drive_total)
        return total_gb if total_gb >= 1 else self._drive_total / (1024**2)

    def _update_graph(self, capture=False):
        if not self._samples:
            return
        xs = [self._x_val(s[2]) for s in self._samples]
        ys = [s[1] for s in self._samples]

        ax = self._ax
        ax.cla()
        self._style_axes()
        ax.set_xlabel(self._x_label(), color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        xmax = self._x_max()
        if xmax:
            ax.set_xlim(0, xmax)

        ax.fill_between(xs, ys, alpha=0.15, color=th("ACCENT"))
        ax.plot(xs, ys, color=th("ACCENT"), linewidth=1.8, marker="o",
                markersize=3.5, markerfacecolor=th("ACCENT2"), markeredgewidth=0)

        pi = ys.index(max(ys))
        ax.annotate(f"Peak\n{ys[pi]:.0f} MB/s",
                    xy=(xs[pi], ys[pi]),
                    xytext=(8, 12), textcoords="offset points",
                    color=th("GREEN"), fontsize=8, fontfamily=FN,
                    arrowprops=dict(arrowstyle="->", color=th("GREEN"), lw=1.2))

        ax.set_title(self._("samples_label").format(n=len(xs), last=ys[-1]),
                     color=th("TEXT_FIXED"), fontsize=10, fontfamily=FN)
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw_idle()

        if "Peak" in self._stat_labels:
            self._stat_labels["Peak"].config(text=f"{max(ys):.1f}")
        if "Average" in self._stat_labels:
            self._stat_labels["Average"].config(text=f"{sum(ys)/len(ys):.1f}")

        if capture and HAS_PIL:
            buf = io.BytesIO()
            self._fig.savefig(buf, format="png", facecolor=th("PANEL"), dpi=72)
            buf.seek(0)
            self._frame_snaps.append(PIL.Image.open(buf).copy())
            buf.close()

    def _finish(self, samples, peak, avg, elapsed):
        self._running = False
        self._btn_start.config(state="normal", fg=th("GREEN"))
        self._btn_stop.config(state="disabled")
        for key, val in (("Peak", f"{peak:.1f}"), ("Average", f"{avg:.1f}"),
                         ("Duration", f"{elapsed:.1f}")):
            if key in self._stat_labels:
                self._stat_labels[key].config(text=val)
        self._status_var.set(
            self._("done_status").format(peak=peak, avg=avg, dur=elapsed)
        )
        self._ax.set_title(
            self._("complete").format(peak=peak, avg=avg),
            color=th("GREEN"), fontsize=10, fontfamily=FN
        )
        self._canvas.draw()

    def _show_error(self, msg):
        self._running = False
        self._btn_start.config(state="normal", fg=th("GREEN"))
        self._btn_stop.config(state="disabled")
        self._error_var.set(f"{self._('error')}: {msg}")
        self._status_var.set(f"{self._('error')}: {msg}")

    # ─── Mouse crosshair ─────────────────────────────────────────────────

    def _on_mouse_move(self, event):
        if not self._samples or event.inaxes != self._ax:
            return
        xs          = [self._x_val(s[2]) for s in self._samples]
        ys          = [s[1] for s in self._samples]
        elapsed_all = [s[0] for s in self._samples]
        xd = event.xdata
        if xd is None:
            return
        idx = min(range(len(xs)), key=lambda i: abs(xs[i] - xd))

        for attr in ("_vline", "_hover_ann"):
            obj = getattr(self, attr)
            if obj:
                try: obj.remove()
                except Exception: pass

        self._vline = self._ax.axvline(x=xs[idx], color=th("WARN"),
                                        linewidth=0.9, linestyle="--", alpha=0.85)
        unit = "GB" if _bytes_to_gb(self._drive_total) >= 1 else "MB"
        self._hover_ann = self._ax.annotate(
            f"{xs[idx]:.2f} {unit} written\n{elapsed_all[idx]:.1f}s elapsed\n{ys[idx]:.1f} MB/s",
            xy=(xs[idx], ys[idx]),
            xytext=(10, -45), textcoords="offset points",
            fontsize=8, fontfamily=FN, color=th("WARN"),
            bbox=dict(boxstyle="round,pad=0.3", fc=th("CARD"),
                      ec=th("WARN"), lw=0.8, alpha=0.92)
        )
        self._canvas.draw_idle()

    def _on_axes_leave(self, event):
        changed = False
        for attr in ("_vline", "_hover_ann"):
            obj = getattr(self, attr)
            if obj:
                try: obj.remove()
                except Exception: pass
                setattr(self, attr, None)
                changed = True
        if changed:
            self._canvas.draw_idle()

    # ─── Export / Load ────────────────────────────────────────────────────

    def _guard_data(self):
        if not self._samples:
            messagebox.showinfo(self._("no_data"), self._("no_data_msg"))
            return False
        return True

    def _do_export_image(self):
        if not self._guard_data():
            return
        dlg = ExportDialog(self, self._("export_result_img"),
                           ["PNG", "JPG", "GIF"], "fill_the_pane_graph", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r   = dlg.result
        fmt = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        dpi  = 100
        orig = self._fig.get_size_inches()
        self._fig.set_size_inches(r["width"] / dpi, r["height"] / dpi)
        self._fig.savefig(path, dpi=dpi, facecolor=th("PANEL"), bbox_inches="tight",
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
                                "Complete a test to capture animation frames.")
            return
        dlg = ExportDialog(self, self._("export_anim_menu"),
                           ["GIF"], "fill_the_pane_anim", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r   = dlg.result
        fmt = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        tw, th_ = r["width"], r["height"]

        frames = [f.resize((tw, th_), PIL.Image.LANCZOS) for f in self._frame_snaps]
        frames[0].save(path, save_all=True, append_images=frames[1:],
                       loop=0, duration=120, optimize=False)
        self._status_var.set(self._("anim_saved").format(path=path))

    def _do_export_report(self):
        if not self._guard_data():
            return
        dlg = ExportDialog(self, self._("export_report_menu"),
                           ["CSV", "XLS", "NUMBERS"], "fill_the_pane_data", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r   = dlg.result
        fmt = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        tb   = self._target_bytes if self._target_bytes > 0 else 1
        rows = [(i+1, s[0], s[1], s[2], s[2]/tb*100)
                for i, s in enumerate(self._samples)]
        hdrs = ["Sample", "Elapsed (s)", "Write Speed (MB/s)", "Bytes Written", "Capacity %"]

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
                messagebox.showinfo("Note",
                    "xlwt not installed — saved as CSV.\nInstall xlwt for true XLS.")
        else:
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdrs)
                for row in rows:
                    w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                row[3], f"{row[4]:.2f}"])
            messagebox.showinfo("Note",
                "Saved as CSV — open with Apple Numbers or rename to .csv.\n"
                "Full .numbers format requires macOS Numbers.")

        self._status_var.set(self._("data_saved").format(path=path))

    def _do_load_data(self):
        """Load a previously saved CSV and restore graph + stats."""
        path = filedialog.askopenfilename(
            title=self._("load_csv_title"),
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return

        samples = []
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    elapsed = float(row.get("Elapsed (s)", 0))
                    speed   = float(row.get("Write Speed (MB/s)", 0))
                    bw      = int(float(row.get("Bytes Written", 0)))
                    samples.append((elapsed, speed, bw))
        except Exception as e:
            messagebox.showerror("Load Failed", f"Could not read CSV:\n{e}")
            return

        if not samples:
            messagebox.showwarning("Empty File", self._("load_csv_invalid"))
            return

        self._samples      = samples
        self._target_bytes = max(s[2] for s in samples)
        self._drive_total  = self._target_bytes  # best estimate from loaded data
        self._frame_snaps  = []

        peak    = max(s[1] for s in samples)
        avg     = sum(s[1] for s in samples) / len(samples)
        elapsed = samples[-1][0]

        for key, val in (("Peak", f"{peak:.1f}"), ("Average", f"{avg:.1f}"),
                         ("Duration", f"{elapsed:.1f}")):
            if key in self._stat_labels:
                self._stat_labels[key].config(text=val)

        self._graph_subtitle.config(text=os.path.basename(path))
        self._update_graph()
        self._ax.set_title(
            self._("complete").format(peak=peak, avg=avg),
            color=th("GREEN"), fontsize=10, fontfamily=FN
        )
        self._canvas.draw()
        self._status_var.set(self._("data_loaded").format(path=path))


    def _do_export_infographic(self):
        """Export an interactive HTML infographic embeddable in a webpage."""
        if not self._guard_data():
            return
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = filedialog.asksaveasfilename(
            title="Save Infographic for Web",
            defaultextension=".html",
            initialfile=f"fill_the_pane_{ts}.html",
            filetypes=[("HTML File", "*.html"), ("All Files", "*.*")]
        )
        if not path:
            return

        import json
        xs_raw = [self._x_val(s[2]) for s in self._samples]
        ys_raw = [s[1]              for s in self._samples]
        el_raw = [s[0]              for s in self._samples]
        bw_raw = [s[2]              for s in self._samples]

        unit   = "GB" if _bytes_to_gb(self._drive_total) >= 1 else "MB"
        x_lbl  = self._x_label()
        peak   = max(ys_raw)
        avg    = sum(ys_raw) / len(ys_raw)
        dur    = el_raw[-1]
        ititle = f"{APP_NAME} v{APP_VERSION} — Write Speed"

        xs_j = json.dumps([round(v, 4) for v in xs_raw])
        ys_j = json.dumps([round(v, 2) for v in ys_raw])
        el_j = json.dumps([round(v, 2) for v in el_raw])

        html = (
            "<!DOCTYPE html>\n"
            "<html lang='en'>\n"
            "<head>\n"
            "<meta charset='UTF-8'>\n"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>\n"
            f"<title>{ititle}</title>\n"
            "<style>\n"
            "*{box-sizing:border-box;margin:0;padding:0}\n"
            "body{background:#0d0f14;color:#e8eaf0;"
            "font-family:'Segoe UI Variable','Inter',sans-serif;padding:24px}\n"
            "h1{font-size:18px;font-weight:600;color:#00d4ff;margin-bottom:4px}\n"
            ".sub{font-size:12px;color:#7a8099;margin-bottom:20px}\n"
            ".sub a{color:#00d4ff}\n"
            ".stats{display:flex;gap:32px;margin-bottom:20px}\n"
            ".sb{display:flex;flex-direction:column;gap:2px}\n"
            ".sv{font-size:22px;font-weight:700}\n"
            ".sl{font-size:11px;color:#7a8099}\n"
            ".pv{color:#39d353}.av{color:#ff9a3c}\n"
            "#cw{position:relative;background:#1a1e2a;border-radius:8px;"
            "padding:16px 16px 36px 52px}\n"
            "canvas{width:100%!important;cursor:crosshair}\n"
            "#tt{position:absolute;display:none;background:#1a1e2a;"
            "border:1px solid #f0c040;border-radius:6px;padding:8px 12px;"
            "font-size:12px;color:#f0c040;pointer-events:none;"
            "line-height:1.6;white-space:nowrap;z-index:10}\n"
            ".xl{text-align:center;font-size:11px;color:#7a8099;margin-top:6px}\n"
            ".yl{position:absolute;left:6px;top:50%;transform:translateY(-50%) rotate(-90deg);"
            "font-size:11px;color:#7a8099;white-space:nowrap}\n"
            ".ft{margin-top:16px;font-size:11px;color:#7a8099}\n"
            "</style>\n"
            "</head>\n"
            "<body>\n"
            f"<h1>{ititle}</h1>\n"
            f"<div class='sub'>Generated by {APP_NAME} v{APP_VERSION}"
            f" &nbsp;&middot;&nbsp; <a href='{GITHUB_URL}' target='_blank'>{GITHUB_URL}</a></div>\n"
            "<div class='stats'>\n"
            f"<div class='sb'><span class='sv pv'>{peak:.1f}</span><span class='sl'>Peak MB/s</span></div>\n"
            f"<div class='sb'><span class='sv av'>{avg:.1f}</span><span class='sl'>Average MB/s</span></div>\n"
            f"<div class='sb'><span class='sv'>{dur:.1f}s</span><span class='sl'>Duration</span></div>\n"
            "</div>\n"
            "<div id='cw'><div class='yl'>Write Speed (MB/s)</div>\n"
            "<canvas id='c'></canvas><div id='tt'></div></div>\n"
            f"<div class='xl'>{x_lbl}</div>\n"
            "<div class='ft'>Hover over the graph to inspect data points.</div>\n"
            "<script>\n"
            f"const XS={xs_j},YS={ys_j},EL={el_j},UNIT='{unit}';\n"
            "const PI=XS.indexOf?YS.indexOf(Math.max(...YS)):0;\n"
            "const cv=document.getElementById('c'),tt=document.getElementById('tt');\n"
            "const cw=document.getElementById('cw');\n"
            "const PL=0,PR=16,PT=16,PB=8;\n"
            "function draw(hi){\n"
            "  const W=cv.clientWidth,H=Math.round(W*9/16);\n"
            "  cv.width=W;cv.height=H;\n"
            "  const ctx=cv.getContext('2d');\n"
            "  const xMx=Math.max(...XS)*1.02,yMx=Math.max(...YS)*1.18;\n"
            "  const px=x=>PL+(x/xMx)*(W-PL-PR);\n"
            "  const py=y=>H-PB-(y/yMx)*(H-PT-PB);\n"
            "  ctx.clearRect(0,0,W,H);\n"
            "  ctx.strokeStyle='#252a38';ctx.lineWidth=0.5;ctx.setLineDash([4,4]);\n"
            "  [0.25,0.5,0.75,1].forEach(r=>{\n"
            "    const yv=yMx*r;\n"
            "    ctx.beginPath();ctx.moveTo(PL,py(yv));ctx.lineTo(W-PR,py(yv));ctx.stroke();\n"
            "    ctx.fillStyle='#7a8099';ctx.font='10px sans-serif';\n"
            "    ctx.textAlign='right';ctx.fillText(Math.round(yv),PL-4,py(yv)+4);\n"
            "  });\n"
            "  [0,0.25,0.5,0.75,1].forEach(r=>{\n"
            "    const xv=xMx*r;\n"
            "    ctx.beginPath();ctx.moveTo(px(xv),PT);ctx.lineTo(px(xv),H-PB);ctx.stroke();\n"
            "    ctx.fillStyle='#7a8099';ctx.textAlign='center';\n"
            "    ctx.fillText(xv.toFixed(1),px(xv),H-PB+12);\n"
            "  });\n"
            "  ctx.setLineDash([]);\n"
            "  ctx.beginPath();ctx.moveTo(px(XS[0]),py(0));\n"
            "  XS.forEach((x,i)=>ctx.lineTo(px(x),py(YS[i])));\n"
            "  ctx.lineTo(px(XS[XS.length-1]),py(0));ctx.closePath();\n"
            "  ctx.fillStyle='rgba(0,212,255,0.12)';ctx.fill();\n"
            "  ctx.beginPath();ctx.strokeStyle='#00d4ff';ctx.lineWidth=2;ctx.lineJoin='round';\n"
            "  XS.forEach((x,i)=>i===0?ctx.moveTo(px(x),py(YS[i])):ctx.lineTo(px(x),py(YS[i])));\n"
            "  ctx.stroke();\n"
            "  XS.forEach((x,i)=>{\n"
            "    ctx.beginPath();ctx.arc(px(x),py(YS[i]),3.5,0,Math.PI*2);\n"
            "    ctx.fillStyle=i===hi?'#f0c040':'#ff6b35';ctx.fill();\n"
            "  });\n"
            "  const px2=px(XS[PI]),py2=py(YS[PI]);\n"
            "  ctx.strokeStyle='#39d353';ctx.lineWidth=1;ctx.setLineDash([3,3]);\n"
            "  ctx.beginPath();ctx.moveTo(px2,py2);ctx.lineTo(px2+10,py2-16);ctx.stroke();\n"
            "  ctx.setLineDash([]);\n"
            "  ctx.fillStyle='#39d353';ctx.font='bold 11px sans-serif';\n"
            "  ctx.textAlign='left';ctx.fillText('Peak '+Math.round(YS[PI])+' MB/s',px2+12,py2-16);\n"
            "  if(hi>=0){\n"
            "    ctx.strokeStyle='rgba(240,192,64,0.8)';ctx.lineWidth=1;ctx.setLineDash([4,4]);\n"
            "    ctx.beginPath();ctx.moveTo(px(XS[hi]),PT);ctx.lineTo(px(XS[hi]),H-PB);ctx.stroke();\n"
            "    ctx.setLineDash([]);\n"
            "  }\n"
            "  cv._px=px;cv._py=py;cv._xMx=xMx;\n"
            "}\n"
            "function nearest(cx){\n"
            "  const r=cv.getBoundingClientRect();\n"
            "  const mx=(cx-r.left)*(cv.width/r.width);\n"
            "  let b=-1,bd=Infinity;\n"
            "  XS.forEach((x,i)=>{const d=Math.abs(cv._px(x)-mx);if(d<bd){bd=d;b=i;}});\n"
            "  return b;\n"
            "}\n"
            "cv.addEventListener('mousemove',e=>{\n"
            "  const i=nearest(e.clientX);if(i<0)return;\n"
            "  draw(i);\n"
            "  const r=cv.getBoundingClientRect(),cwr=cw.getBoundingClientRect();\n"
            "  const cpx=cv._px(XS[i])*(r.width/cv.width);\n"
            "  const cpy=cv._py(YS[i])*(r.height/cv.height);\n"
            "  let lx=r.left-cwr.left+cpx+12;\n"
            "  const tw=tt.offsetWidth||160;\n"
            "  if(lx+tw>cw.offsetWidth-8)lx=r.left-cwr.left+cpx-tw-12;\n"
            "  tt.style.left=lx+'px';\n"
            "  tt.style.top=(r.top-cwr.top+cpy-50)+'px';\n"
            "  tt.style.display='block';\n"
            "  tt.innerHTML=XS[i].toFixed(2)+' '+UNIT+' written<br>'+EL[i].toFixed(1)+'s elapsed<br>'+YS[i].toFixed(1)+' MB/s';\n"
            "});\n"
            "cv.addEventListener('mouseleave',()=>{tt.style.display='none';draw(-1);});\n"
            "new ResizeObserver(()=>draw(-1)).observe(cv);\n"
            "draw(-1);\n"
            "</script>\n"
            "</body>\n"
            "</html>"
        )
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            self._status_var.set(f"Infographic saved \u2192 {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def _show_about(self):
        AboutDialog(self, self._lang)


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = FillThePane()
    app.mainloop()
