"""
Fill the Pane  v0.11
Sequential Write Torture Test
https://github.com/jiyang1018/Fill_the_Pane
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import time
import csv
import shutil
import platform
import datetime
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
APP_NAME     = "Fill the Pane"
APP_SUBTITLE = "Sequential Write Torture Test"
APP_VERSION  = "0.11"
BUILD_DT     = "2025-05-01 00:00:00"
GITHUB_URL   = "https://github.com/jiyang1018/Fill_the_Pane"
AUTHOR       = "Yang Ji"
LICENSE_STR  = "GNU General Public License v3.0 (GPLv3)"

# ═══════════════════════════════════════════════════════════════════════════
#  Theme system  (dark / light)
# ═══════════════════════════════════════════════════════════════════════════

DARK_THEME = {
    "BG":      "#0d0f14",
    "PANEL":   "#13161e",
    "CARD":    "#1a1e2a",
    "ACCENT":  "#00d4ff",
    "ACCENT2": "#ff6b35",
    "TEXT":    "#e8eaf0",
    "SUBTEXT": "#7a8099",
    "GREEN":   "#39d353",
    "RED_C":   "#e05555",
    "WARN":    "#f0c040",
    "BORDER":  "#252a38",
    "RED_VAL": "#ff4444",
}

LIGHT_THEME = {
    "BG":      "#f0f2f5",
    "PANEL":   "#ffffff",
    "CARD":    "#e8ecf2",
    "ACCENT":  "#0077cc",
    "ACCENT2": "#e05000",
    "TEXT":    "#1a1a2e",
    "SUBTEXT": "#5a6070",
    "GREEN":   "#1a8a34",
    "RED_C":   "#cc2222",
    "WARN":    "#b07000",
    "BORDER":  "#c8cdd8",
    "RED_VAL": "#cc0000",
}

# Active theme dict — mutated on theme switch
TH = dict(DARK_THEME)

def th(key):
    return TH[key]

# ═══════════════════════════════════════════════════════════════════════════
#  Fonts  (Inter Regular 400, with bold variants)
# ═══════════════════════════════════════════════════════════════════════════
FN = "Inter"   # Falls back gracefully to system sans-serif on Windows if Inter not installed

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

# ISO 639-3 codes + native name + flag
LANGUAGES = [
    ("ENG", "English",              "English",              "🇺🇸"),
    ("DAN", "Danish",               "Dansk",                "🇩🇰"),
    ("DEU", "German",               "Deutsch",              "🇩🇪"),
    ("FIN", "Finnish",              "Suomi",                "🇫🇮"),
    ("FRA", "French",               "Français",             "🇫🇷"),
    ("HUN", "Hungarian",            "Magyar",               "🇭🇺"),
    ("IND", "Indonesian",           "Bahasa Indonesia",     "🇮🇩"),
    ("MSA", "Malay",                "Bahasa Melayu",        "🇲🇾"),
    ("NLD", "Dutch",                "Nederlands",           "🇳🇱"),
    ("NOR", "Norwegian",            "Norsk",                "🇳🇴"),
    ("POL", "Polish",               "Polski",               "🇵🇱"),
    ("POR", "Portuguese",           "Português",            "🇵🇹"),
    ("RON", "Romanian",             "Română",               "🇷🇴"),
    ("RUS", "Russian",              "Русский",              "🇷🇺"),
    ("SPA", "Spanish",              "Español",              "🇪🇸"),
    ("SWE", "Swedish",              "Svenska",              "🇸🇪"),
    ("TUR", "Turkish",              "Türkçe",               "🇹🇷"),
    ("UKR", "Ukrainian",            "Українська",           "🇺🇦"),
    ("VIE", "Vietnamese",           "Tiếng Việt",           "🇻🇳"),
    ("ARA", "Arabic",               "العربية",              "🇸🇦"),
    ("ZHO", "Chinese (Simplified)", "简体中文",              "🇨🇳"),
    ("ZHT", "Chinese (Traditional)","繁體中文",              "🇹🇼"),
    ("JPN", "Japanese",             "日本語",               "🇯🇵"),
    ("KOR", "Korean",               "한국어",               "🇰🇷"),
]

EN = {
    "title":              "Fill the Pane",
    "subtitle":           "Sequential Write Torture Test",
    "select_drive":       "Select Drive",
    "refresh_drives":     "↺  Refresh Drives",
    "drive_info_btn":     "Drive Info",
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
    "export_menu":        "Export",
    "language_menu":      "Language",
    "theme_menu":         "Theme",
    "dark_mode":          "Dark Mode",
    "light_mode":         "Light Mode",
    "about_menu":         "About",
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
    "capacity_pct_axis":  "Capacity Filled (%)",
    "exceed_warn":        "Fill target exceeds free space.",
}

TRANSLATIONS = {
    "English": EN,
    "German": {**EN,
        "subtitle": "Sequentieller Schreib-Belastungstest",
        "refresh_drives": "↺  Laufwerke Aktualisieren",
        "start_test": "▶  Test Starten", "stop_test": "■  Test Stoppen",
        "save_image": "🖼  Grafik Speichern", "save_data": "📊  Daten Speichern",
        "capacity_pct_axis": "Kapazität Gefüllt (%)",
    },
    "French": {**EN,
        "subtitle": "Test de Torture d'Écriture Séquentielle",
        "refresh_drives": "↺  Actualiser les Lecteurs",
        "start_test": "▶  Démarrer le Test", "stop_test": "■  Arrêter le Test",
        "save_image": "🖼  Enregistrer l'Image", "save_data": "📊  Enregistrer les Données",
        "capacity_pct_axis": "Capacité Remplie (%)",
    },
    "Spanish": {**EN,
        "subtitle": "Prueba de Tortura de Escritura Secuencial",
        "refresh_drives": "↺  Actualizar Unidades",
        "start_test": "▶  Iniciar Prueba", "stop_test": "■  Detener Prueba",
        "save_image": "🖼  Guardar Imagen", "save_data": "📊  Guardar Datos",
        "capacity_pct_axis": "Capacidad Llenada (%)",
    },
    "Japanese": {**EN,
        "subtitle": "シーケンシャル書き込み耐久テスト",
        "start_test": "▶  テスト開始", "stop_test": "■  テスト停止",
        "save_image": "🖼  グラフ保存", "save_data": "📊  データ保存",
        "capacity_pct_axis": "容量充填率 (%)",
    },
    "Chinese (Simplified)": {**EN,
        "subtitle": "顺序写入压力测试",
        "start_test": "▶  开始测试", "stop_test": "■  停止测试",
        "save_image": "🖼  保存图表", "save_data": "📊  保存数据",
        "capacity_pct_axis": "容量填充 (%)",
    },
    "Korean": {**EN,
        "subtitle": "순차 쓰기 고문 테스트",
        "start_test": "▶  테스트 시작", "stop_test": "■  테스트 중지",
        "save_image": "🖼  그래프 저장", "save_data": "📊  데이터 저장",
        "capacity_pct_axis": "용량 채움 (%)",
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
        info[Tr(lang, "total_capacity")] = _fmt_size(total)
        info[Tr(lang, "used_space")]     = _fmt_size(used)
        info[Tr(lang, "free_space")]     = _fmt_size(free)
        info[Tr(lang, "usage_pct")]      = f"{used/total*100:.1f}%"
    except Exception:
        pass
    if HAS_PSUTIL and part_obj:
        info[Tr(lang, "mount_point")] = part_obj.mountpoint
        info[Tr(lang, "device")]      = part_obj.device
        info[Tr(lang, "file_system")] = part_obj.fstype or "Unknown"
        opts = part_obj.opts or ""
        info[Tr(lang, "options")]     = opts if opts else "—"
    if platform.system() == "Windows":
        try:
            import ctypes
            vol = ctypes.create_unicode_buffer(261)
            ser = ctypes.c_ulong()
            fsn = ctypes.create_unicode_buffer(261)
            ctypes.windll.kernel32.GetVolumeInformationW(
                mountpoint, vol, 261, ctypes.byref(ser), None, None, fsn, 261
            )
            if vol.value:
                info[Tr(lang, "volume_name")] = vol.value
            info[Tr(lang, "serial_number")] = f"{ser.value:08X}"
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
                           font=FONT_SMALL(), fg=th("TEXT"), bg=th("BG"),
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
                  bg=th("GREEN"), fg=th("BG"), relief="flat", padx=14, pady=5,
                  command=self._ok).pack(side="left", padx=8)
        tk.Button(br, text=Tr(self._lang, "cancel_btn"), font=FONT_BTN(),
                  bg=th("CARD"), fg=th("TEXT"), relief="flat", padx=14, pady=5,
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
        self.title(Tr(lang, "drive_info_title"))
        self.configure(bg=th("BG"))
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text=Tr(lang, "drive_info_title"),
                 font=FONT_HEADER(), fg=th("ACCENT"), bg=th("BG")).pack(pady=(16, 8))

        frm = tk.Frame(self, bg=th("CARD"), highlightthickness=1,
                       highlightbackground=th("BORDER"))
        frm.pack(fill="both", padx=20, pady=(0, 8))
        for k, v in info_dict.items():
            r = tk.Frame(frm, bg=th("CARD"))
            r.pack(fill="x", padx=12, pady=3)
            tk.Label(r, text=k, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=18, anchor="w").pack(side="left")
            tk.Label(r, text=str(v), font=FONT_SMALL(), fg=th("TEXT"),
                     bg=th("CARD"), anchor="e").pack(side="right")

        tk.Button(self, text="Close", font=FONT_BTN(), bg=th("CARD"), fg=th("TEXT"),
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
        self.configure(bg=th("BG"))
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text=APP_NAME, font=(FN, 18, "bold"),
                 fg=th("ACCENT"), bg=th("BG")).pack(pady=(20, 2))
        tk.Label(self, text=APP_SUBTITLE, font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG")).pack()
        tk.Label(self, text=f"Version {APP_VERSION}", font=FONT_SMALL(),
                 fg=th("TEXT"), bg=th("BG")).pack(pady=(8, 2))
        tk.Label(self, text=f"Build: {BUILD_DT}", font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG")).pack()

        tk.Frame(self, bg=th("BORDER"), height=1).pack(fill="x", padx=20, pady=12)

        tk.Label(self, text=f"Author: {AUTHOR}", font=FONT_SMALL(),
                 fg=th("TEXT"), bg=th("BG")).pack()
        tk.Label(self, text=LICENSE_STR, font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG")).pack(pady=(4, 0))

        lnk = tk.Label(self, text=GITHUB_URL, font=FONT_SMALL(),
                       fg=th("ACCENT"), bg=th("BG"), cursor="hand2")
        lnk.pack(pady=(4, 14))
        lnk.bind("<Button-1>", lambda e: __import__("webbrowser").open(GITHUB_URL))

        tk.Button(self, text="Close", font=FONT_BTN(), bg=th("CARD"), fg=th("TEXT"),
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
        self._lang         = "English"
        self._worker       = None
        self._samples      = []   # (elapsed, mb_s, bytes_written)
        self._running      = False
        self._fill_var     = tk.DoubleVar(value=90.0)
        self._drive_var    = tk.StringVar()
        self._drives       = []
        self._target_bytes = 0
        self._frame_snaps  = []
        self._vline        = None
        self._hover_ann    = None

        self.title(f"{APP_NAME}  —  {APP_SUBTITLE}")
        self.configure(bg=th("BG"))
        self.resizable(True, True)
        self.minsize(960, 660)
        self._build_ui()
        self._refresh_drives()
        self.after(200, self._center_window)

    def _(self, key):
        return Tr(self._lang, key)

    # ─── Window ───────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 1100, 720
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    # ─── Build UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_menubar()

        # Title bar
        tb = tk.Frame(self, bg=th("BG"), pady=7)
        tb.pack(fill="x", padx=18)
        tk.Label(tb, text="⬡ " + self._("title"),
                 font=FONT_TITLE(), fg=th("ACCENT"), bg=th("BG")).pack(side="left")
        tk.Label(tb, text="  —  " + self._("subtitle"),
                 font=FONT_SMALL(), fg=th("SUBTEXT"), bg=th("BG")).pack(side="left", pady=3)

        # Body
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

        # Status bar
        self._status_var = tk.StringVar(value=self._("ready"))
        tk.Label(self, textvariable=self._status_var, font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("BG"), anchor="w").pack(fill="x", padx=20, pady=(0, 4))

    def _build_menubar(self):
        mb = tk.Menu(self, bg=th("PANEL"), fg=th("TEXT"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     relief="flat", font=FONT_MENU())
        self.config(menu=mb)
        self._menubar = mb

        # Export
        em = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("export_menu"), menu=em)
        em.add_command(label=self._("export_result_img"),  command=self._do_export_image)
        em.add_command(label=self._("export_anim_menu"),   command=self._do_export_animation)
        em.add_command(label=self._("export_report_menu"), command=self._do_export_report)

        # Language — show native name in that language
        lm = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("language_menu"), menu=lm)
        for iso, eng, native, flag in LANGUAGES:
            lm.add_command(
                label=f"{flag}  {iso}  {native}",
                command=lambda n=eng: self._set_language(n)
            )

        # Theme
        tm = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("theme_menu"), menu=tm)
        tm.add_command(label=self._("dark_mode"),  command=lambda: self._set_theme("dark"))
        tm.add_command(label=self._("light_mode"), command=lambda: self._set_theme("light"))

        mb.add_command(label=self._("about_menu"), command=self._show_about)

    def _build_left(self, p):
        def sec(text, ref=None):
            lbl = tk.Label(p, text=text, font=FONT_SEC(),
                     fg=th("ACCENT"), bg=th("PANEL"), anchor="w")
            lbl.pack(fill="x", padx=14, pady=(10, 2))
            if ref is not None:
                ref.append(lbl)
            return lbl

        def btn(text, cmd, color):
            b = tk.Button(p, text=text, font=FONT_BTN(), bg=th("CARD"), fg=color,
                          activebackground=th("BORDER"), activeforeground=color,
                          relief="flat", bd=0, cursor="hand2", pady=6,
                          command=cmd, highlightthickness=1,
                          highlightbackground=th("BORDER"))
            return b

        # ── Select Drive ──
        sec("Select Drive")
        dr = tk.Frame(p, bg=th("PANEL"))
        dr.pack(fill="x", padx=14, pady=(0, 3))
        tk.Label(dr, text="💾", font=(FN, 13), bg=th("PANEL"),
                 fg=th("ACCENT")).pack(side="left", padx=(0, 4))
        self._drive_menu = ttk.Combobox(dr, textvariable=self._drive_var,
                                         state="readonly", font=FONT_SMALL())
        self._drive_menu.pack(side="left", fill="x", expand=True)

        self._style_ttk()

        btn(self._("refresh_drives"), self._refresh_drives, th("SUBTEXT")).pack(
            fill="x", padx=14, pady=(2, 2))
        btn(self._("drive_info_btn"), self._show_drive_info, th("ACCENT")).pack(
            fill="x", padx=14, pady=(0, 8))

        # ── Fill Target ──
        sec("Fill Target")
        fr = tk.Frame(p, bg=th("PANEL"))
        fr.pack(fill="x", padx=14, pady=(0, 2))
        tk.Label(fr, text="Write Up To", font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="left")
        self._fill_label = tk.Label(fr, text="90%", font=FONT_STAT(),
                                     fg=th("ACCENT"), bg=th("PANEL"), width=5)
        self._fill_label.pack(side="right")
        tk.Scale(p, from_=10, to=90, orient="horizontal",
                 variable=self._fill_var, bg=th("PANEL"), fg=th("TEXT"),
                 troughcolor=th("CARD"), activebackground=th("ACCENT"),
                 highlightthickness=0, bd=0, sliderlength=18,
                 command=self._on_fill_change, font=FONT_SMALL()
                 ).pack(fill="x", padx=14, pady=(0, 8))

        # ── Drive Info card ──
        sec("Drive Info")
        self._info_frame = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                                     highlightbackground=th("BORDER"))
        self._info_frame.pack(fill="x", padx=14, pady=(0, 8))
        self._info_labels    = {}
        self._info_raw_vals  = {}   # store raw numbers for red-highlight check

        for key in ("Total", "Free", "Target Write"):
            r = tk.Frame(self._info_frame, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=3)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=13, anchor="w").pack(side="left")
            lbl = tk.Label(r, text="—", font=FONT_SMALL(), fg=th("TEXT"),
                           bg=th("CARD"), anchor="e")
            lbl.pack(side="right")
            self._info_labels[key] = lbl

        # ── Results card ──
        sec("Results")
        sfrm = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                        highlightbackground=th("BORDER"))
        sfrm.pack(fill="x", padx=14, pady=(0, 8))
        self._stat_labels = {}
        for key, unit in (("Peak", "MB/s"), ("Average", "MB/s"), ("Duration", "sec")):
            r = tk.Frame(sfrm, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=4)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=10, anchor="w").pack(side="left")
            tk.Label(r, text=unit, font=FONT_UNIT(), fg=th("SUBTEXT"),
                     bg=th("CARD")).pack(side="right")
            val = tk.Label(r, text="—", font=FONT_STAT(), fg=th("ACCENT2"), bg=th("CARD"))
            val.pack(side="right")
            self._stat_labels[key] = val

        # ── Action buttons ──
        self._btn_start = btn(self._("start_test"), self._start, th("GREEN"))
        self._btn_start.pack(fill="x", padx=14, pady=(4, 3))
        self._btn_stop  = btn(self._("stop_test"),  self._stop,  th("RED_C"))
        self._btn_stop.pack(fill="x", padx=14, pady=(0, 8))
        self._btn_stop.config(state="disabled")

        # ── Export buttons ──
        btn(self._("save_image"),     self._do_export_image,     th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("save_animation"), self._do_export_animation, th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn(self._("save_data"),      self._do_export_report,    th("ACCENT")).pack(fill="x", padx=14, pady=(0, 10))

        self._drive_menu.bind("<<ComboboxSelected>>", self._on_drive_select)

    def _build_graph(self, p):
        hdr = tk.Frame(p, bg=th("PANEL"))
        hdr.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(hdr, text="Write Speed Over Time",
                 font=FONT_HEADER(), fg=th("TEXT"), bg=th("PANEL")).pack(side="left")
        self._graph_subtitle = tk.Label(hdr, text="", font=FONT_SMALL(),
                                         fg=th("SUBTEXT"), bg=th("PANEL"))
        self._graph_subtitle.pack(side="right")

        # Progress bar
        prog_outer = tk.Frame(p, bg=th("PANEL"))
        prog_outer.pack(fill="x", padx=14, pady=(6, 0))
        self._prog_var = tk.DoubleVar(value=0)
        self._prog_bar = ttk.Progressbar(prog_outer, variable=self._prog_var,
                                          maximum=100,
                                          style="DM.Horizontal.TProgressbar")
        self._prog_bar.pack(fill="x")
        self._pct_lbl = tk.Label(prog_outer, text="0%",
                                  font=(FN, 8, "bold"), fg="white", bg=th("PANEL"))
        self._pct_lbl.place(relx=0.5, rely=0.5, anchor="center")
        self._prog_bar.bind("<Configure>",
            lambda e: self._pct_lbl.place(in_=self._prog_bar,
                                           relx=0.5, rely=0.5, anchor="center"))

        self._prog_detail = tk.Label(p, text="", font=FONT_SMALL(),
                                      fg=th("SUBTEXT"), bg=th("PANEL"))
        self._prog_detail.pack(anchor="w", padx=14, pady=(2, 4))

        # Matplotlib figure
        self._fig = Figure(figsize=(6, 4), facecolor=th("PANEL"))
        self._ax  = self._fig.add_subplot(111)
        self._style_axes()
        self._canvas = FigureCanvasTkAgg(self._fig, master=p)
        self._canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        self._canvas.mpl_connect("axes_leave_event",    self._on_axes_leave)
        self._canvas.draw()

    # ─── TTK style ────────────────────────────────────────────────────────

    def _style_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=th("CARD"), background=th("CARD"),
                        foreground=th("TEXT"), selectbackground=th("BORDER"),
                        selectforeground=th("TEXT"), bordercolor=th("BORDER"),
                        arrowcolor=th("ACCENT"))
        style.configure("DM.Horizontal.TProgressbar",
                        troughcolor=th("CARD"), background=th("ACCENT"),
                        bordercolor=th("BORDER"), lightcolor=th("ACCENT"),
                        darkcolor=th("ACCENT"), thickness=20)

    # ─── Axes style ───────────────────────────────────────────────────────

    def _style_axes(self):
        ax = self._ax
        ax.set_facecolor(th("CARD"))
        ax.tick_params(colors=th("SUBTEXT"), labelsize=9)
        ax.spines[:].set_color(th("BORDER"))
        # X axis: capacity filled %
        ax.set_xlabel(self._("capacity_pct_axis"), color=th("SUBTEXT"),
                      fontsize=9, fontfamily=FN)
        ax.set_ylabel("Write Speed (MB/s)", color=th("SUBTEXT"),
                      fontsize=9, fontfamily=FN)
        ax.grid(True, color=th("BORDER"), linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_title(self._("waiting"), color=th("SUBTEXT"), fontsize=10, fontfamily=FN)
        self._fig.set_facecolor(th("PANEL"))
        self._fig.tight_layout(pad=1.5)

    # ─── Theme switch ─────────────────────────────────────────────────────

    def _set_theme(self, mode):
        TH.clear()
        TH.update(DARK_THEME if mode == "dark" else LIGHT_THEME)
        messagebox.showinfo(
            "Theme Changed",
            f"{'Dark' if mode == 'dark' else 'Light'} mode applied.\n\nRestart the app to fully apply the theme."
        )

    # ─── Language ─────────────────────────────────────────────────────────

    def _set_language(self, lang):
        self._lang = lang
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
        fill   = self._fill_var.get() / 100.0
        target = int(total * fill)
        exceeds = target > free

        # Clamp actual write target for safety
        clamped = min(target, int(free * 0.98))

        self._info_labels["Total"].config(
            text=_fmt_size(total), fg=th("TEXT"))
        self._info_labels["Free"].config(
            text=_fmt_size(free),
            fg=th("RED_VAL") if exceeds else th("TEXT"))
        self._info_labels["Target Write"].config(
            text=_fmt_size(target),
            fg=th("RED_VAL") if exceeds else th("TEXT"))

        # Grey out / re-enable Start Test
        if exceeds:
            self._btn_start.config(state="disabled", fg=th("SUBTEXT"))
            self._status_var.set(self._("exceed_warn"))
        else:
            self._btn_start.config(state="normal", fg=th("GREEN"))
            self._status_var.set(self._("ready"))

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

    def _capacity_pct(self, bytes_written):
        """Convert bytes written → % of total target (for X axis)."""
        tb = self._target_bytes if self._target_bytes > 0 else 1
        return bytes_written / tb * 100.0

    def _update_graph(self, capture=False):
        if not self._samples:
            return
        # X = capacity filled %, Y = MB/s
        xs = [self._capacity_pct(s[2]) for s in self._samples]
        ys = [s[1] for s in self._samples]

        ax = self._ax
        ax.cla()
        self._style_axes()
        ax.fill_between(xs, ys, alpha=0.15, color=th("ACCENT"))
        ax.plot(xs, ys, color=th("ACCENT"), linewidth=1.8, marker="o",
                markersize=3.5, markerfacecolor=th("ACCENT2"), markeredgewidth=0)
        ax.set_xlim(0, 100)

        pi = ys.index(max(ys))
        ax.annotate(f"Peak\n{ys[pi]:.0f} MB/s",
                    xy=(xs[pi], ys[pi]),
                    xytext=(8, 12), textcoords="offset points",
                    color=th("ACCENT2"), fontsize=8, fontfamily=FN,
                    arrowprops=dict(arrowstyle="->", color=th("ACCENT2"), lw=1.2))

        ax.set_title(self._("samples_label").format(n=len(xs), last=ys[-1]),
                     color=th("TEXT"), fontsize=10, fontfamily=FN)
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
        self._prog_var.set(100)
        self._pct_lbl.config(text="100%")
        self._pct_lbl.place(in_=self._prog_bar, relx=0.5, rely=0.5, anchor="center")
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
        self._status_var.set(f"{self._('error')}: {msg}")
        messagebox.showerror("Benchmark Error", msg)

    # ─── Mouse crosshair  (shows elapsed time in tooltip) ─────────────────

    def _on_mouse_move(self, event):
        if not self._samples or event.inaxes != self._ax:
            return
        # xs on graph = capacity %, but we need to find nearest sample
        xs = [self._capacity_pct(s[2]) for s in self._samples]
        ys = [s[1] for s in self._samples]
        elapsed_all = [s[0] for s in self._samples]

        xd = event.xdata
        if xd is None:
            return
        idx = min(range(len(xs)), key=lambda i: abs(xs[i] - xd))

        for attr in ("_vline", "_hover_ann"):
            obj = getattr(self, attr)
            if obj:
                try:
                    obj.remove()
                except Exception:
                    pass

        self._vline = self._ax.axvline(x=xs[idx], color=th("WARN"),
                                        linewidth=0.9, linestyle="--", alpha=0.85)
        # Tooltip: capacity % + elapsed time
        self._hover_ann = self._ax.annotate(
            f"{xs[idx]:.1f}% filled\n{elapsed_all[idx]:.1f}s elapsed\n{ys[idx]:.1f} MB/s",
            xy=(xs[idx], ys[idx]),
            xytext=(10, -40), textcoords="offset points",
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
                try:
                    obj.remove()
                except Exception:
                    pass
                setattr(self, attr, None)
                changed = True
        if changed:
            self._canvas.draw_idle()

    # ─── Export ───────────────────────────────────────────────────────────

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
                                "Complete or run a test to capture animation frames.")
            return
        dlg = ExportDialog(self, self._("export_anim_menu"),
                           ["GIF", "MP4"], "fillthepane_anim", self._lang)
        self.wait_window(dlg)
        if not dlg.result:
            return
        r   = dlg.result
        fmt = r["format"].lower()
        path = r["path"]
        if not path.lower().endswith(f".{fmt}"):
            path += f".{fmt}"
        tw, th_ = r["width"], r["height"]

        if fmt == "gif":
            frames = [f.resize((tw, th_), PIL.Image.LANCZOS) for f in self._frame_snaps]
            frames[0].save(path, save_all=True, append_images=frames[1:],
                           loop=0, duration=120, optimize=False)
            self._status_var.set(self._("anim_saved").format(path=path))
        else:
            try:
                import matplotlib.animation as manim
                fd = [(self._capacity_pct(s[2]), s[1]) for s in self._samples]
                fig2, ax2 = plt.subplots(facecolor=th("PANEL"))
                ax2.set_facecolor(th("CARD"))
                ax2.tick_params(colors=th("SUBTEXT"))
                ax2.spines[:].set_color(th("BORDER"))
                line, = ax2.plot([], [], color=th("ACCENT"), linewidth=1.8)
                ax2.set_xlim(0, 100)
                ax2.set_ylim(0, max(s[1] for s in fd) * 1.2)
                ax2.set_xlabel(self._("capacity_pct_axis"), color=th("SUBTEXT"), fontsize=9)
                ax2.set_ylabel("MB/s", color=th("SUBTEXT"), fontsize=9)
                fig2.tight_layout()

                def _anim(i):
                    line.set_data([fd[j][0] for j in range(i+1)],
                                  [fd[j][1] for j in range(i+1)])
                    return line,

                ani = manim.FuncAnimation(fig2, _anim, frames=len(fd),
                                          interval=100, blit=True)
                dpi2 = max(72, min(tw, th_) // 4)
                ani.save(path, writer=manim.FFMpegWriter(fps=10, codec="libx265"), dpi=dpi2)
                plt.close(fig2)
                self._status_var.set(self._("anim_saved").format(path=path))
            except Exception as e:
                messagebox.showerror("MP4 Failed",
                    f"Could not export MP4.\nEnsure ffmpeg is installed.\n\n{e}")

    def _do_export_report(self):
        if not self._guard_data():
            return
        dlg = ExportDialog(self, self._("export_report_menu"),
                           ["CSV", "XLS", "NUMBERS"], "fillthepane_data", self._lang)
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
                messagebox.showinfo("Note",
                    "xlwt not installed — saved as CSV.\nInstall xlwt for true XLS.")
        else:  # numbers
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

    def _show_about(self):
        AboutDialog(self, self._lang)


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = FillThePane()
    app.mainloop()
