"""
Fill the Pane  v0.4.9
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
import json
import glob
import base64
TOGGLE_OFF_B64 = "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"
TOGGLE_ON_B64  = "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"


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
APP_VERSION  = "0.4.9"
BUILD_DT     = "2025-05-01 00:00:00"
GITHUB_URL   = "https://github.com/jiyang1018/Fill_the_Pane"
AUTHOR       = "Yang Ji"
LICENSE_STR  = "GNU General Public License v3.0 (GPLv3)"

# ═══════════════════════════════════════════════════════════════════════════
#  Settings
# ═══════════════════════════════════════════════════════════════════════════

def _app_base():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def _settings_path():
    return os.path.join(_app_base(), "settings.ini")

def _languages_path():
    return os.path.join(_app_base(), "languages.json")

def _results_dir():
    d = os.path.join(_app_base(), "results")
    os.makedirs(d, exist_ok=True)
    return d

def load_languages():
    """Load translations from languages.json, fall back to built-in EN only."""
    path = _languages_path()
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

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
    "start_test": "Start Test",
    "stop_test": "Stop Test",
    "save_image": "Save Graph Image",
    "save_animation": "Save Animation",
    "save_data": "Save Data",
    "load_data": "Load Data",
    "save_infographic": "Infographic for Web",
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
    "write_speed_mbs":    "Write Speed (MB/s)",
    "pct_of_capacity":    "% of Total Capacity",
    "target_gb_label":    "Target (GB):",
    "target_gb_hint":     "← type & press Enter",
    "peak_annotation":    "Peak",
}

TRANSLATIONS = {
    "English": EN,
    "German": {**EN,
        "subtitle":       "Sequentieller Schreib-Belastungstest",
        "refresh_drives": "↺  Laufwerke Aktualisieren",
        "start_test": "Test Starten",
        "stop_test": "Test Stoppen",
        "save_image": "Grafik Speichern",
        "save_data": "Daten Speichern",
        "load_data": "Daten Laden",
        "capacity_axis":  "Geschriebene Laufwerkskapazität",
    },
    "French": {**EN,
        "subtitle":       "Test de Torture d'Écriture Séquentielle",
        "refresh_drives": "↺  Actualiser les Lecteurs",
        "start_test": "Démarrer le Test",
        "stop_test": "Arrêter le Test",
        "save_image": "Enregistrer l'Image",
        "save_data": "Enregistrer les Données",
        "load_data": "Charger les Données",
        "capacity_axis":  "Capacité du Lecteur Écrite",
    },
    "Spanish": {**EN,
        "subtitle":       "Prueba de Tortura de Escritura Secuencial",
        "refresh_drives": "↺  Actualizar Unidades",
        "start_test": "Iniciar Prueba",
        "stop_test": "Detener Prueba",
        "save_image": "Guardar Imagen",
        "save_data": "Guardar Datos",
        "load_data": "Cargar Datos",
        "capacity_axis":  "Capacidad del Disco Escrita",
    },
    "Japanese": {**EN,
        "subtitle":       "シーケンシャル書き込み耐久テスト",
        "start_test": "テスト開始",
        "stop_test": "テスト停止",
        "save_image": "グラフ保存",
        "save_data": "データ保存",
        "load_data": "データ読込",
        "capacity_axis":  "書き込み済み容量",
    },
    "Chinese (Simplified)": {**EN,
        "subtitle":       "顺序写入压力测试",
        "start_test": "开始测试",
        "stop_test": "停止测试",
        "save_image": "保存图表",
        "save_data": "保存数据",
        "load_data": "加载数据",
        "capacity_axis":  "已写入容量",
    },
    "Korean": {**EN,
        "subtitle":       "순차 쓰기 고문 테스트",
        "start_test": "테스트 시작",
        "stop_test": "테스트 중지",
        "save_image": "그래프 저장",
        "save_data": "데이터 저장",
        "load_data": "데이터 불러오기",
        "capacity_axis":  "드라이브 용량 기록",
    },
}
for _iso, _eng, _native, _flag in LANGUAGES:
    if _eng not in TRANSLATIONS:
        TRANSLATIONS[_eng] = EN

# Merge external languages.json over built-in translations at startup
_EXT_LANGS = load_languages()
for _lname, _ldata in _EXT_LANGS.items():
    if _lname in TRANSLATIONS:
        TRANSLATIONS[_lname] = {**TRANSLATIONS[_lname], **_ldata}
    else:
        TRANSLATIONS[_lname] = {**EN, **_ldata}


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
#  Benchmark worker  — true CDM SEQ1M Q8T1
#  Windows: single thread, 8 outstanding OVERLAPPED async writes,
#           FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH (unbuffered)
#           4 KB-aligned 1 MB buffers — identical to CrystalDiskMark
#  Non-Windows fallback: sequential buffered writes, Q1T1
# ═══════════════════════════════════════════════════════════════════════════

CHUNK            = 1 * 1024 * 1024    # 1 MB per I/O request — CDM SEQ1M
QUEUE_DEPTH      = 8                   # 8 outstanding requests — CDM Q8
SECTOR_SIZE      = 4096               # alignment for NO_BUFFERING
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
        # Round DOWN to a multiple of CHUNK so every write is exactly 1 MB
        tb = (tb // CHUNK) * CHUNK
        self.target_bytes = tb

        min_needed = CHUNK * QUEUE_DEPTH
        if tb < min_needed:
            self.on_error(
                f"Not enough free space.\nFree: {_fmt_size(free)}, "
                f"needed: {_fmt_size(min_needed)}"
            )
            return

        ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        tmp = os.path.join(self.target_dir, f"_FtP_{ts}.tmp")
        # Remove any leftover _FtP_*.tmp files on this drive
        for stale in glob.glob(os.path.join(self.target_dir, "_FtP_*.tmp")):
            try: os.remove(stale)
            except Exception: pass

        if platform.system() == "Windows":
            self._run_windows(tmp, tb)
        else:
            self._run_fallback(tmp, tb)

    # ── Windows: true OVERLAPPED Q8T1 ────────────────────────────────────

    def _run_windows(self, tmp, tb):
        """
        Single thread issues QUEUE_DEPTH async WriteFile calls via OVERLAPPED
        structures, keeping exactly 8 requests in flight at all times.
        File opened with FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH
        to bypass the Windows cache — identical to CrystalDiskMark.
        """
        import ctypes
        import ctypes.wintypes as wt

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        # ── Win32 constants ──────────────────────────────────────────────
        GENERIC_WRITE            = 0x40000000
        FILE_SHARE_READ          = 0x00000001
        CREATE_ALWAYS            = 2
        FILE_FLAG_NO_BUFFERING   = 0x20000000
        FILE_FLAG_WRITE_THROUGH  = 0x80000000
        FILE_FLAG_OVERLAPPED     = 0x40000000
        INVALID_HANDLE_VALUE     = ctypes.c_void_p(-1).value
        INFINITE                 = 0xFFFFFFFF
        STATUS_PENDING           = 0x00000103
        ERROR_IO_PENDING         = 997

        flags = (FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH |
                 FILE_FLAG_OVERLAPPED)

        # ── OVERLAPPED structure ─────────────────────────────────────────
        class OVERLAPPED(ctypes.Structure):
            class _OffsetUnion(ctypes.Union):
                class _OffsetStruct(ctypes.Structure):
                    _fields_ = [("Offset", wt.DWORD), ("OffsetHigh", wt.DWORD)]
                _fields_ = [("s", _OffsetStruct), ("Pointer", ctypes.c_void_p)]
            _fields_ = [
                ("Internal",     ctypes.c_size_t),
                ("InternalHigh", ctypes.c_size_t),
                ("u",            _OffsetUnion),
                ("hEvent",       wt.HANDLE),
            ]

        # ── Set explicit argtypes to prevent integer overflow ─────────────
        kernel32.WriteFile.argtypes = [
            wt.HANDLE, ctypes.c_void_p, wt.DWORD,
            ctypes.POINTER(wt.DWORD), ctypes.c_void_p
        ]
        kernel32.WriteFile.restype = wt.BOOL
        kernel32.GetOverlappedResult.argtypes = [
            wt.HANDLE, ctypes.c_void_p,
            ctypes.POINTER(wt.DWORD), wt.BOOL
        ]
        kernel32.GetOverlappedResult.restype = wt.BOOL
        kernel32.WaitForMultipleObjects.argtypes = [
            wt.DWORD, ctypes.c_void_p, wt.BOOL, wt.DWORD
        ]
        kernel32.WaitForMultipleObjects.restype = wt.DWORD
        kernel32.ResetEvent.argtypes  = [wt.HANDLE]
        kernel32.ResetEvent.restype   = wt.BOOL
        kernel32.CloseHandle.argtypes = [wt.HANDLE]
        kernel32.CloseHandle.restype  = wt.BOOL
        kernel32.CreateEventW.argtypes = [
            ctypes.c_void_p, wt.BOOL, wt.BOOL, ctypes.c_wchar_p
        ]
        kernel32.CreateEventW.restype = wt.HANDLE
        VirtualAlloc = kernel32.VirtualAlloc
        VirtualAlloc.argtypes = [
            ctypes.c_void_p, ctypes.c_size_t, wt.DWORD, wt.DWORD
        ]
        VirtualAlloc.restype = ctypes.c_void_p
        VirtualFree = kernel32.VirtualFree
        VirtualFree.argtypes  = [ctypes.c_void_p, ctypes.c_size_t, wt.DWORD]
        VirtualFree.restype   = wt.BOOL

        # ── Open file ────────────────────────────────────────────────────
        hFile = kernel32.CreateFileW(
            tmp,
            GENERIC_WRITE,
            FILE_SHARE_READ,
            None,
            CREATE_ALWAYS,
            flags,
            None
        )
        if hFile == INVALID_HANDLE_VALUE:
            err = ctypes.get_last_error()
            self.on_error(f"CreateFile failed (error {err}). "
                          f"Try running as Administrator.")
            return

        # ── Allocate sector-aligned 1 MB buffers (one per queue slot) ───
        # ctypes.create_string_buffer is not guaranteed aligned;
        # allocate via VirtualAlloc for guaranteed 4 KB alignment.
        MEM_COMMIT   = 0x1000
        MEM_RESERVE  = 0x2000
        MEM_RELEASE  = 0x8000
        PAGE_READWRITE = 0x04

        bufs = []
        raw_data = os.urandom(CHUNK)
        for _ in range(QUEUE_DEPTH):
            ptr = VirtualAlloc(None, CHUNK, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
            if not ptr:
                self.on_error("VirtualAlloc failed — out of memory.")
                kernel32.CloseHandle(hFile)
                return
            ctypes.memmove(ptr, raw_data, CHUNK)
            bufs.append(ptr)

        # ── Create one event per slot for OVERLAPPED ─────────────────────
        events = []
        for _ in range(QUEUE_DEPTH):
            ev = kernel32.CreateEventW(None, True, False, None)
            events.append(ev)

        ovls = [OVERLAPPED() for _ in range(QUEUE_DEPTH)]
        for i, (ovl, ev) in enumerate(zip(ovls, events)):
            ovl.hEvent = ev

        # ── Slot state ───────────────────────────────────────────────────
        # slot_offset[i] = file offset currently being written by slot i
        # None = slot is idle
        slot_offset = [None] * QUEUE_DEPTH
        next_offset  = 0          # next file offset to issue
        bytes_confirmed = 0       # bytes whose WriteFile has been GetOverlappedResult'd

        samples        = []
        t0             = time.perf_counter()
        t_interval     = t0
        interval_bytes = 0

        def _issue(slot):
            nonlocal next_offset
            if next_offset >= tb or self._stop.is_set():
                return False
            off = next_offset
            next_offset += CHUNK
            ovl = ovls[slot]
            # Reset event and set file offset in OVERLAPPED
            kernel32.ResetEvent(events[slot])
            ovl.u.s.Offset     = off & 0xFFFFFFFF
            ovl.u.s.OffsetHigh = (off >> 32) & 0xFFFFFFFF
            written = wt.DWORD(0)
            ok = kernel32.WriteFile(
                hFile,
                ctypes.c_void_p(bufs[slot]),
                wt.DWORD(CHUNK),
                ctypes.byref(written),
                ctypes.byref(ovl)
            )
            err = ctypes.get_last_error()
            if not ok and err != ERROR_IO_PENDING:
                return False
            slot_offset[slot] = off
            return True

        def _collect(slot, block=False):
            """Wait for slot to complete; return bytes written or 0."""
            nonlocal bytes_confirmed, interval_bytes
            timeout = INFINITE if block else 0
            transferred = wt.DWORD(0)
            ok = kernel32.GetOverlappedResult(
                hFile, ctypes.byref(ovls[slot]),
                ctypes.byref(transferred), wt.BOOL(block)
            )
            if ok:
                n = transferred.value
                bytes_confirmed += n
                interval_bytes  += n
                slot_offset[slot] = None
                return n
            return 0

        # ── Pre-warm: write at END of file to warm up drive write path ──────
        # CDM warms the drive before measuring. We write QUEUE_DEPTH x 1 MB
        # at the very end of the target region so the real test (starting at
        # offset 0) hits cold sectors and measures accurately.
        pw_start = max(0, tb - CHUNK * QUEUE_DEPTH)
        prewarm_offset = [pw_start]
        def _issue_prewarm(slot):
            if prewarm_offset[0] >= tb:
                return False
            off = prewarm_offset[0]
            prewarm_offset[0] += CHUNK
            kernel32.ResetEvent(events[slot])
            ovls[slot].u.s.Offset     = off & 0xFFFFFFFF
            ovls[slot].u.s.OffsetHigh = (off >> 32) & 0xFFFFFFFF
            written = wt.DWORD(0)
            kernel32.WriteFile(hFile, ctypes.c_void_p(bufs[slot]),
                               wt.DWORD(CHUNK), ctypes.byref(written),
                               ctypes.byref(ovls[slot]))
            slot_offset[slot] = off
            return True

        for s in range(QUEUE_DEPTH):
            _issue_prewarm(s)
        for s in range(QUEUE_DEPTH):
            if slot_offset[s] is not None:
                _collect(s, block=True)
                slot_offset[s] = None

        # Reset state — real measurement starts now from offset 0
        next_offset     = 0
        bytes_confirmed = 0
        interval_bytes  = 0
        t0              = time.perf_counter()
        t_interval      = t0

        try:
            # Fill all queue slots initially
            for s in range(QUEUE_DEPTH):
                _issue(s)

            while not self._stop.is_set():
                # Wait for ANY slot to finish (WaitForMultipleObjects)
                handles = (wt.HANDLE * QUEUE_DEPTH)(*events)
                WAIT_OBJECT_0 = 0
                idx = kernel32.WaitForMultipleObjects(
                    wt.DWORD(QUEUE_DEPTH), handles, wt.BOOL(False), wt.DWORD(50)
                )

                now = time.perf_counter()

                # Collect all completed slots
                for s in range(QUEUE_DEPTH):
                    if slot_offset[s] is not None:
                        _collect(s, block=False)
                        if slot_offset[s] is None:
                            # slot finished — reissue if space remains
                            _issue(s)

                # Speed sample
                if now - t_interval >= MEASURE_INTERVAL:
                    elapsed = now - t0
                    dt = now - t_interval
                    mb_s = (interval_bytes / dt) / (1024 * 1024) if dt > 0 else 0
                    if mb_s > 0:
                        samples.append((elapsed, mb_s, bytes_confirmed))
                        self.on_sample(elapsed, mb_s, bytes_confirmed, tb)
                        self.on_progress(bytes_confirmed, tb, mb_s)
                    t_interval     = now
                    interval_bytes = 0

                # All slots idle and no more data to write → done
                if all(s is None for s in slot_offset) and next_offset >= tb:
                    break

            # Drain any remaining in-flight slots
            for s in range(QUEUE_DEPTH):
                if slot_offset[s] is not None:
                    _collect(s, block=True)

        finally:
            kernel32.CloseHandle(hFile)
            for ev in events:
                kernel32.CloseHandle(ev)
            for ptr in bufs:
                VirtualFree(ctypes.c_void_p(ptr), ctypes.c_size_t(0), wt.DWORD(MEM_RELEASE))
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
        if not self._stop.is_set():
            self.on_progress(tb, tb, avg)
        else:
            self.on_progress(bytes_confirmed, tb, avg)
        self.on_done(samples, peak, avg, total_elapsed)

    # ── Non-Windows fallback: sequential buffered Q1T1 ────────────────────

    def _run_fallback(self, tmp, tb):
        data = os.urandom(CHUNK)
        samples        = []
        bytes_written  = 0
        t0             = time.perf_counter()
        t_interval     = t0
        interval_bytes = 0
        try:
            with open(tmp, "wb") as f:
                while bytes_written < tb and not self._stop.is_set():
                    remaining  = tb - bytes_written
                    write_size = min(CHUNK, remaining)
                    f.write(data[:write_size])
                    bytes_written  += write_size
                    interval_bytes += write_size
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
                    f.flush()
                    os.fsync(f.fileno())
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
            self.on_error("No data collected.")
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
            initialdir=_results_dir(),
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
        self._fill_min     = 1     # minimum fill %, recomputed on drive select
        self._target_gb_var    = tk.StringVar(value="")
        self._fill_pct_precise  = None  # set by GB entry; None = use slider
        self._drive_var    = tk.StringVar()
        self._drives       = []
        self._target_bytes = 0
        self._drive_total  = 0
        self._frame_snaps  = []
        self._vline        = None
        self._hover_ann    = None
        self._notes_var    = tk.StringVar(value="")
        self._theme_toggle = tk.BooleanVar(value=(_theme_mode == 'light'))

        self.title(f"{APP_NAME} v{APP_VERSION}  —  {APP_SUBTITLE}")
        self.configure(bg=th("BG"))
        self.resizable(True, True)
        self.minsize(960, 800)
        self._build_ui()
        self._refresh_drives()
        self.after(200, self._center_window)

    def _(self, key):
        return Tr(self._lang, key)

    def _center_window(self):
        self.update_idletasks()
        w, h = 1160, 900
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    # ─── Build UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_menubar()

        tb = tk.Frame(self, bg=th("BG"), pady=7)
        tb.pack(fill="x", padx=18)
        tk.Label(tb, text="⬡ " + self._("title"),
                 font=FONT_TITLE(), fg=th("ACCENT"), bg=th("BG")).pack(side="left")
        tk.Label(tb, text=f"  v{APP_VERSION}",
                 font=FONT_TITLE(), fg=th("SUBTEXT"), bg=th("BG")).pack(side="left")

        # Theme toggle — right side of title bar
        self._toggle_canvas = tk.Canvas(tb, width=52, height=28, bg=th("BG"),
                                         highlightthickness=0, cursor="hand2")
        self._toggle_canvas.pack(side="right", padx=(0, 4), pady=4)
        tk.Label(tb, text="☀" if self._theme_mode == "light" else "🌙",
                 font=(FN, 11), bg=th("BG"), fg=th("SUBTEXT"),
                 cursor="hand2").pack(side="right", padx=(0, 4))
        self._draw_toggle()
        self._toggle_canvas.bind("<Button-1>", self._on_theme_toggle)

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

        # Language menu
        lm = tk.Menu(mb, tearoff=0, bg=th("PANEL"), fg=th("TEXT_FIXED"),
                     activebackground=th("CARD"), activeforeground=th("ACCENT"),
                     font=FONT_MENU())
        mb.add_cascade(label=self._("language_menu"), menu=lm)
        for iso, eng, native, flag in LANGUAGES:
            lm.add_command(
                label=f"{flag}  {native}",
                command=lambda n=eng: self._set_language(n)
            )

        # About menu
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
        sec(self._("select_drive"))
        dr = tk.Frame(p, bg=th("PANEL"))
        dr.pack(fill="x", padx=14, pady=(0, 3))
        self._drive_menu = ttk.Combobox(dr, textvariable=self._drive_var,
                                         state="readonly", font=FONT_SMALL())
        self._drive_menu.pack(side="left", fill="x", expand=True)
        self._style_ttk()

        btn(self._("refresh_drives"), self._refresh_drives, th("SUBTEXT")).pack(
            fill="x", padx=14, pady=(2, 8))

        # ── Fill Target
        sec(self._("fill_target"))

        # Row 1: "Write Up To" label + percentage display (0.1% precision)
        fr = tk.Frame(p, bg=th("PANEL"))
        fr.pack(fill="x", padx=14, pady=(0, 2))
        tk.Label(fr, text=self._("write_up_to"), font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="left")
        self._fill_label = tk.Label(fr, text="90.0%", font=FONT_STAT(),
                                     fg=th("ACCENT"), bg=th("PANEL"), width=6)
        self._fill_label.pack(side="right")

        # Custom canvas slider — red zone for used space
        self._slider_canvas = tk.Canvas(p, height=28, bg=th("PANEL"),
                                         highlightthickness=0, cursor="hand2")
        self._slider_canvas.pack(fill="x", padx=14, pady=(0, 2))
        self._slider_canvas.bind("<Configure>",  lambda e: self._draw_fill_slider())
        self._slider_canvas.bind("<Button-1>",   self._on_slider_click)
        self._slider_canvas.bind("<B1-Motion>",  self._on_slider_click)

        # Tick labels
        tick_row = tk.Frame(p, bg=th("PANEL"))
        tick_row.pack(fill="x", padx=14, pady=(0, 4))
        tk.Label(tick_row, text="0%", font=(FN, 8), fg=th("SUBTEXT"),
                 bg=th("PANEL")).pack(side="left")
        tk.Label(tick_row, text="100%", font=(FN, 8), fg=th("SUBTEXT"),
                 bg=th("PANEL")).pack(side="right")

        # Row 2: Manual GB entry — user can type exact value
        gb_row = tk.Frame(p, bg=th("PANEL"))
        gb_row.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(gb_row, text=self._("target_gb_label"), font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="left")
        self._target_gb_var = tk.StringVar(value="")
        self._target_gb_entry = tk.Entry(gb_row, textvariable=self._target_gb_var,
                 font=FONT_SMALL(), bg=th("CARD"), fg=th("TEXT_FIXED"),
                 insertbackground=th("TEXT_FIXED"), relief="flat", bd=4, width=8,
                 justify="right")
        self._target_gb_entry.pack(side="right")
        self._target_gb_entry.bind("<Return>",   self._on_target_gb_enter)
        self._target_gb_entry.bind("<FocusOut>", self._on_target_gb_enter)
        tk.Label(gb_row, text="  " + self._("target_gb_hint"), font=(FN, 8),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="right")

        # ── Drive Info card
        sec(self._("drive_info_sec"))
        self._info_frame = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                                     highlightbackground=th("BORDER"))
        self._info_frame.pack(fill="x", padx=14, pady=(0, 8))
        self._info_labels = {}
        _info_keys = [
            (self._("total"),        "Total"),
            (self._("free"),         "Free"),
            (self._("target_write"), "Target Write"),
        ]
        for key, _internal in _info_keys:
            r = tk.Frame(self._info_frame, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=3)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=13, anchor="w").pack(side="left")
            lbl = tk.Label(r, text="—", font=FONT_SMALL(), fg=th("TEXT_FIXED"),
                           bg=th("CARD"), anchor="e")
            lbl.pack(side="right")
            self._info_labels[_internal] = lbl

        # ── Results card
        sec(self._("results"))
        sfrm = tk.Frame(p, bg=th("CARD"), highlightthickness=1,
                        highlightbackground=th("BORDER"))
        sfrm.pack(fill="x", padx=14, pady=(0, 8))
        self._stat_labels = {}
        # Peak = green, Average = orange, Duration = black/light
        stat_colors = {"Peak": th("GREEN"), "Average": th("ORANGE"), "Duration": th("TEXT_FIXED")}
        _stat_keys = [
            (self._("peak"),     "Peak",     self._("mb_s")),
            (self._("average"),  "Average",  self._("mb_s")),
            (self._("duration"), "Duration", self._("sec")),
        ]
        for key, _internal, unit in _stat_keys:
            r = tk.Frame(sfrm, bg=th("CARD"))
            r.pack(fill="x", padx=10, pady=4)
            tk.Label(r, text=key, font=FONT_SMALL(), fg=th("SUBTEXT"),
                     bg=th("CARD"), width=10, anchor="w").pack(side="left")
            tk.Label(r, text=unit, font=FONT_UNIT(), fg=th("SUBTEXT"),
                     bg=th("CARD")).pack(side="right")
            val = tk.Label(r, text="—", font=FONT_STAT(),
                           fg=stat_colors[_internal], bg=th("CARD"))
            val.pack(side="right")
            self._stat_labels[_internal] = val

        # ── Error label (sits above Start Test)
        self._error_var = tk.StringVar(value="")
        self._error_lbl = tk.Label(p, textvariable=self._error_var,
                                    font=FONT_SMALL(), fg=th("RED_VAL"),
                                    bg=th("PANEL"), anchor="w", wraplength=260)
        self._error_lbl.pack(fill="x", padx=14, pady=(4, 0))

        # ── Action buttons
        self._btn_start = btn("▶  " + self._("start_test"), self._start, th("GREEN"))
        self._btn_start.pack(fill="x", padx=14, pady=(2, 3))
        self._btn_stop  = btn("■  " + self._("stop_test"),  self._stop,  th("RED_C"))
        self._btn_stop.pack(fill="x", padx=14, pady=(0, 8))
        self._btn_stop.config(state="disabled")

        # ── Export/Load buttons — icons hardcoded, translations are plain text
        btn("🖼  " + self._("save_image"),       self._do_export_image,       th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("🎬  " + self._("save_animation"),   self._do_export_animation,   th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("💾  " + self._("save_data"),        self._do_export_report,      th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("📂  " + self._("load_data"),        self._do_load_data,          th("ACCENT")).pack(fill="x", padx=14, pady=(0, 3))
        btn("🌐  " + self._("save_infographic"), self._do_export_infographic, th("ACCENT")).pack(fill="x", padx=14, pady=(0, 10))

        self._drive_menu.bind("<<ComboboxSelected>>", self._on_drive_select)

    def _build_graph(self, p):
        hdr = tk.Frame(p, bg=th("PANEL"))
        hdr.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(hdr, text=self._("write_speed"),
                 font=FONT_HEADER(), fg=th("TEXT_FIXED"), bg=th("PANEL")).pack(side="left")
        self._graph_subtitle = tk.Label(hdr, text="", font=FONT_SMALL(),
                                         fg=th("SUBTEXT"), bg=th("PANEL"))
        self._graph_subtitle.pack(side="right")

        # Notes field
        notes_row = tk.Frame(p, bg=th("PANEL"))
        notes_row.pack(fill="x", padx=14, pady=(4, 0))
        tk.Label(notes_row, text="Notes:", font=FONT_SMALL(),
                 fg=th("SUBTEXT"), bg=th("PANEL")).pack(side="left", padx=(0, 6))
        tk.Entry(notes_row, textvariable=self._notes_var, font=FONT_SMALL(),
                 bg=th("CARD"), fg=th("TEXT_FIXED"), insertbackground=th("TEXT_FIXED"),
                 relief="flat", bd=4).pack(side="left", fill="x", expand=True)

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
        # Persistent plot objects — updated in place, no cla() during live test
        self._plot_line  = None
        self._plot_fill  = None
        self._plot_peak  = None
        self._plot_ax2   = None
        self._canvas.draw()

    def _on_graph_resize(self, event):
        w_px, h_px = event.width, event.height
        if w_px < 10 or h_px < 10:
            return
        dpi = self._fig.get_dpi()
        self._fig.set_size_inches(w_px / dpi, h_px / dpi, forward=False)
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw_idle()

    # ─── Styling ──────────────────────────────────────────────────────────

    def _style_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=th("CARD"), background=th("CARD"),
                        foreground=th("TEXT_FIXED"), selectbackground=th("ACCENT"),
                        selectforeground="#000000", bordercolor=th("BORDER"),
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
                x_label += f"  (GB  /  % of {total_gb:.1f} GB)"
            else:
                x_label += f"  (MB  /  % of {self._drive_total/(1024**2):.0f} MB)"
        ax.set_xlabel(x_label, color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        ax.set_ylabel(self._("write_speed_mbs"), color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        ax.grid(True, color=th("BORDER"), linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_title(self._("waiting"), color=th("SUBTEXT"), fontsize=10, fontfamily=FN)
        self._fig.set_facecolor(th("PANEL"))
        self._fig.tight_layout(pad=1.5)

    # ─── Theme ────────────────────────────────────────────────────────────

    def _draw_toggle(self):
        import tkinter as _tk
        c = self._toggle_canvas
        c.delete("all")
        is_light = self._theme_mode == "light"
        b64 = TOGGLE_ON_B64 if is_light else TOGGLE_OFF_B64
        data = base64.b64decode(b64)
        import io as _io
        from PIL import Image as _Img, ImageTk as _ITk
        img = _Img.open(_io.BytesIO(data)).resize((52, 28), _Img.LANCZOS)
        # Store reference to prevent GC
        self._toggle_img = _ITk.PhotoImage(img)
        c.config(width=52, height=28)
        c.create_image(0, 0, anchor="nw", image=self._toggle_img)

    def _on_theme_toggle(self, event=None):
        new_mode = "light" if self._theme_mode == "dark" else "dark"
        self._set_theme(new_mode)

    def _set_theme(self, mode):
        if mode == self._theme_mode:
            return
        self._theme_mode = mode
        self._theme_toggle.set(mode == "light")
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
        prev_mp = None
        idx = self._drive_menu.current()
        if idx >= 0 and idx < len(self._drives):
            prev_mp = self._drives[idx][1]
        self._drives = get_drives()
        self._drive_menu["values"] = [d[0] for d in self._drives]
        if not self._drives:
            return
        new_idx = 0
        if prev_mp:
            for i, d in enumerate(self._drives):
                if d[1] == prev_mp:
                    new_idx = i
                    break
        self._drive_menu.current(new_idx)
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
        self._fill_min = max(1, min(math.ceil(used_pct + 1), 89))  # never >= 90
        self._slider_used_pct = used_pct

        # Clamp current slider value into [_fill_min, 90.0]
        current = self._fill_var.get()
        if current < self._fill_min:
            self._fill_var.set(float(self._fill_min))
        elif current > 90.0:
            self._fill_var.set(90.0)

        # Use precise pct if set by GB entry, otherwise use slider integer
        pct_now = self._effective_pct()
        self._fill_label.config(text=f"{pct_now:.1f}%")
        # Only sync GB entry if precise value was NOT user-typed (avoid overwriting)
        if not (hasattr(self, '_fill_pct_precise') and self._fill_pct_precise is not None):
            self._sync_gb_entry(pct_now)

        fill    = pct_now / 100.0
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

        # Reset graph when drive changes (keep notes)
        if hasattr(self, "_prev_drive_mp") and self._prev_drive_mp != mp:
            self._samples = []
            self._frame_snaps = []
            self._plot_line = None
            self._plot_fill = None
            self._plot_peak = None
            self._plot_ax2  = None
            for lbl in self._stat_labels.values():
                lbl.config(text="—")
            self._write_status_var.set("")
            self._graph_subtitle.config(text="")
        self._prev_drive_mp = mp
        self.after(10, self._draw_fill_slider)
        self._ax.cla()
        self._style_axes()
        self._canvas.draw_idle()

    def _draw_fill_slider(self):
        c = self._slider_canvas
        c.delete("all")
        W = c.winfo_width()
        if W < 10:
            return
        H, TY, TH = 28, 11, 6
        used_pct = getattr(self, "_slider_used_pct", 0)
        fill_min = getattr(self, "_fill_min", 1)
        cur_pct  = self._effective_pct()

        def px(pct):
            return max(0, min(W, int(pct / 100 * W)))

        # Track background
        c.create_rectangle(0, TY, W, TY + TH,
                           fill=th("CARD"), outline="", width=0)
        # Red zone: 0 to fill_min (used + buffer)
        if fill_min > 0:
            c.create_rectangle(0, TY, px(fill_min), TY + TH,
                               fill=th("RED_VAL"), outline="", width=0)
        # Thumb
        tx = px(cur_pct)
        c.create_oval(tx - 8, H//2 - 8, tx + 8, H//2 + 8,
                      fill=th("ACCENT"), outline=th("PANEL"), width=2)

    def _on_slider_click(self, event):
        W = self._slider_canvas.winfo_width()
        if W < 10:
            return
        pct = max(0, min(100, event.x / W * 100))
        v = int(round(pct))
        v = max(self._fill_min, min(90, v))
        self._fill_var.set(v)
        self._fill_pct_precise = None
        self._fill_label.config(text=f"{float(v):.1f}%")
        self._sync_gb_entry(float(v))
        self._draw_fill_slider()
        self._on_drive_select(None)

    def _on_fill_change(self, val):
        v = int(float(val))
        if v < self._fill_min:
            v = self._fill_min
            self._fill_var.set(v)
        elif v > 90:
            v = 90
            self._fill_var.set(v)
        self._fill_pct_precise = None
        pct = float(v)
        self._fill_label.config(text=f"{pct:.1f}%")
        self._sync_gb_entry(pct)
        self._draw_fill_slider()
        self._on_drive_select(None)

    def _effective_pct(self):
        """Return the fill % to actually use.
        Prefers _fill_pct_precise (set by GB entry) over slider integer."""
        if hasattr(self, '_fill_pct_precise') and self._fill_pct_precise is not None:
            return self._fill_pct_precise
        return float(self._fill_var.get())

    def _sync_gb_entry(self, pct):
        """Update the GB entry to reflect the current percentage."""
        if self._drive_total > 0:
            total_gb = self._drive_total / (1024 ** 3)
            gb = pct / 100.0 * total_gb
            try:
                self._target_gb_var.set(f"{gb:.2f}")
            except AttributeError:
                pass

    def _on_target_gb_enter(self, event=None):
        """User typed a GB value — use it as the precise target.
        Slider snaps to nearest whole % visually but the GB value is preserved."""
        if self._drive_total <= 0:
            return
        try:
            gb = float(self._target_gb_var.get())
        except ValueError:
            return
        total_gb = self._drive_total / (1024 ** 3)
        if total_gb <= 0:
            return
        pct = gb / total_gb * 100.0
        # Clamp pct to valid range
        min_gb = float(self._fill_min) / 100.0 * total_gb
        max_gb = 90.0 / 100.0 * total_gb
        gb = max(min_gb, min(max_gb, gb))
        pct = gb / total_gb * 100.0
        # Snap slider to nearest whole number (display only)
        self._fill_var.set(int(round(pct)))
        # Store precise pct separately so _effective_pct() picks it up
        self._fill_pct_precise = pct
        self._fill_label.config(text=f"{pct:.1f}%")
        # Keep GB entry showing exactly what user typed (clamped)
        self._target_gb_var.set(f"{gb:.2f}")
        self._on_drive_select(None)

    # ─── Benchmark ────────────────────────────────────────────────────────

    def _start(self):
        idx = self._drive_menu.current()
        if idx < 0:
            messagebox.showwarning(self._("no_drive"), self._("no_drive_msg"))
            return
        _, mp, total, free, _ = self._drives[idx]
        self._drive_total = total
        fill   = self._effective_pct() / 100.0
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
        self._plot_line = None
        self._plot_fill = None
        self._plot_peak = None
        self._plot_ax2  = None
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
        eta_str = ""
        if mb_s > 0 and bw < total:
            remaining_bytes = total - bw
            eta_sec = remaining_bytes / (mb_s * 1024 * 1024)
            if eta_sec < 60:
                eta_str = f"   ETA {eta_sec:.0f}s"
            elif eta_sec < 3600:
                eta_str = f"   ETA {int(eta_sec//60)}m {int(eta_sec%60)}s"
            else:
                eta_str = f"   ETA {int(eta_sec//3600)}h {int((eta_sec%3600)//60)}m"
        self._write_status_var.set(
            f"{_fmt_size(bw)} / {_fmt_size(total)}  ({pct:.1f}%)   {mb_s:.1f} MB/s{eta_str}"
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

    def _full_redraw(self):
        """Full axes redraw — used on reset, theme change, and load. Not called during live test."""
        self._plot_line = None
        self._plot_fill = None
        self._plot_peak = None
        self._plot_ax2  = None
        ax = self._ax
        ax.cla()
        self._style_axes()
        xmax = self._x_max()
        if xmax:
            ax.set_xlim(0, xmax)
        ax.set_xlabel(self._x_label(), color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
        if self._drive_total > 0 and xmax:
            tv = xmax
            self._plot_ax2 = ax.secondary_xaxis('top',
                functions=(lambda x: x / tv * 100, lambda x: x * tv / 100))
            self._plot_ax2.set_xlabel("% of Total Capacity", color=th("SUBTEXT"),
                                       fontsize=8, fontfamily=FN)
            self._plot_ax2.tick_params(colors=th("SUBTEXT"), labelsize=8)
        self._fig.tight_layout(pad=1.5)
        self._canvas.draw()

    def _update_graph(self, capture=False):
        if not self._samples:
            return
        xs = [self._x_val(s[2]) for s in self._samples]
        ys = [s[1] for s in self._samples]
        xmax = self._x_max()
        ax = self._ax

        if self._plot_line is None:
            # First sample — do a full setup, create persistent objects
            ax.cla()
            self._style_axes()
            ax.set_xlabel(self._x_label(), color=th("SUBTEXT"), fontsize=9, fontfamily=FN)
            if xmax:
                ax.set_xlim(0, xmax)
            if self._drive_total > 0 and xmax:
                tv = xmax
                self._plot_ax2 = ax.secondary_xaxis('top',
                    functions=(lambda x: x / tv * 100, lambda x: x * tv / 100))
                self._plot_ax2.set_xlabel(self._("pct_of_capacity"), color=th("SUBTEXT"),
                                           fontsize=8, fontfamily=FN)
                self._plot_ax2.tick_params(colors=th("SUBTEXT"), labelsize=8)
            self._plot_fill, = [ax.fill_between(xs, ys, alpha=0.15, color=th("ACCENT"))]
            self._plot_line, = ax.plot(xs, ys, color=th("ACCENT"), linewidth=1.8,
                                        marker="o", markersize=3.5,
                                        markerfacecolor=th("ACCENT2"), markeredgewidth=0)
            pi = ys.index(max(ys))
            self._plot_peak = ax.annotate(f"{self._('peak_annotation')}\n{ys[pi]:.0f} MB/s",
                        xy=(xs[pi], ys[pi]), xytext=(8, 12),
                        textcoords="offset points",
                        color=th("GREEN"), fontsize=8, fontfamily=FN,
                        arrowprops=dict(arrowstyle="->", color=th("GREEN"), lw=1.2))
            ax.set_title(self._("samples_label").format(n=len(xs), last=ys[-1]),
                         color=th("TEXT_FIXED"), fontsize=10, fontfamily=FN)
            self._fig.tight_layout(pad=1.5)
        else:
            # Subsequent samples — update data in place, minimal redraw
            self._plot_line.set_data(xs, ys)

            # Update fill — remove old, add new (fill_between can't be updated in place)
            if self._plot_fill:
                self._plot_fill.remove()
            self._plot_fill = ax.fill_between(xs, ys, alpha=0.15, color=th("ACCENT"))

            # Update peak annotation
            pi = ys.index(max(ys))
            if self._plot_peak:
                self._plot_peak.remove()
            self._plot_peak = ax.annotate(f"{self._('peak_annotation')}\n{ys[pi]:.0f} MB/s",
                        xy=(xs[pi], ys[pi]), xytext=(8, 12),
                        textcoords="offset points",
                        color=th("GREEN"), fontsize=8, fontfamily=FN,
                        arrowprops=dict(arrowstyle="->", color=th("GREEN"), lw=1.2))

            # Auto-scale y
            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True)
            if xmax:
                ax.set_xlim(0, xmax)
            ax.set_title(self._("samples_label").format(n=len(xs), last=ys[-1]),
                         color=th("TEXT_FIXED"), fontsize=10, fontfamily=FN)

        self._canvas.draw_idle()

        if "Peak" in self._stat_labels:
            self._stat_labels["Peak"].config(text=f"{max(ys):.1f}")
        if "Average" in self._stat_labels:
            self._stat_labels["Average"].config(text=f"{sum(ys)/len(ys):.1f}")

        if capture and HAS_PIL:
            buf = io.BytesIO()
            orig_in = self._fig.get_size_inches()
            self._fig.set_size_inches(12.8, 7.2, forward=False)
            _notes = self._notes_var.get().strip()
            _nt = self._fig.text(0.5, 0.01, _notes, ha="center",
                va="bottom", fontsize=9, color=th("SUBTEXT"),
                fontfamily=FN) if _notes else None
            self._fig.savefig(buf, format="png", facecolor=th("PANEL"),
                              dpi=72, bbox_inches="tight")
            if _nt: _nt.remove()
            self._fig.set_size_inches(*orig_in, forward=False)
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
        notes = self._notes_var.get().strip()
        complete_title = self._("complete").format(peak=peak, avg=avg)
        if notes:
            complete_title += f"  |  {notes}"
        self._ax.set_title(complete_title, color=th("GREEN"), fontsize=10, fontfamily=FN)
        # Replace ETA with total elapsed time in the status line
        tb = self._target_bytes if self._target_bytes > 0 else 1
        pct = min(100.0, (samples[-1][2] / tb * 100) if samples else 100.0)
        bw  = samples[-1][2] if samples else tb
        if elapsed < 60:
            elapsed_str = f"   Total {elapsed:.1f}s"
        elif elapsed < 3600:
            elapsed_str = f"   Total {int(elapsed//60)}m {int(elapsed%60)}s"
        else:
            elapsed_str = f"   Total {int(elapsed//3600)}h {int((elapsed%3600)//60)}m"
        self._write_status_var.set(
            f"{_fmt_size(bw)} / {_fmt_size(tb)}  ({pct:.1f}%)   {peak:.1f} MB/s peak{elapsed_str}"
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
            if self._vline or self._hover_ann:
                for attr in ("_vline", "_hover_ann"):
                    obj = getattr(self, attr)
                    if obj:
                        try: obj.remove()
                        except Exception: pass
                        setattr(self, attr, None)
                if self._samples:
                    self._plot_line = None
                    self._plot_fill = None
                    self._plot_peak = None
                    self._plot_ax2  = None
                    self._update_graph()
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
        xmax = self._x_max() or 1
        pct_written = xs[idx] / xmax * 100.0 if xmax > 0 else 0
        self._hover_ann = self._ax.annotate(
            f"{xs[idx]:.2f} {unit} written  ({pct_written:.1f}%)\n{elapsed_all[idx]:.1f}s elapsed\n{ys[idx]:.1f} MB/s",
            xy=(xs[idx], ys[idx]),
            xytext=(10, -45), textcoords="offset points",
            fontsize=8, fontfamily=FN, color=th("WARN"),
            bbox=dict(boxstyle="round,pad=0.3", fc=th("CARD"),
                      ec=th("WARN"), lw=0.8, alpha=0.92)
        )
        self._canvas.draw_idle()

    def _on_axes_leave(self, event):
        for attr in ("_vline", "_hover_ann"):
            obj = getattr(self, attr)
            if obj:
                try: obj.remove()
                except Exception: pass
                setattr(self, attr, None)
        if self._samples:
            # Reset persistent plot objects so _update_graph does a clean redraw
            self._plot_line = None
            self._plot_fill = None
            self._plot_peak = None
            self._plot_ax2  = None
            self._update_graph()

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
        notes = self._notes_var.get().strip()
        if notes:
            self._fig.text(0.5, 0.01, notes, ha='center', va='bottom',
                           fontsize=9, color=th("SUBTEXT"), fontfamily=FN,
                           transform=self._fig.transFigure)
        self._fig.savefig(path, dpi=dpi, facecolor=th("PANEL"), bbox_inches="tight",
                          format="jpeg" if fmt == "jpg" else fmt)
        if notes:
            self._fig.texts.clear()
        self._fig.set_size_inches(*orig)
        self._canvas.draw_idle()
        self._status_var.set(self._("graph_saved").format(path=path))

    def _do_export_animation(self):
        if not self._guard_data():
            return
        if not HAS_PIL:
            messagebox.showwarning("Pillow Required", self._("anim_unavail"))
            return
        # If no live frames (loaded data), regenerate frames from samples
        if len(self._frame_snaps) < 2 and self._samples:
            self._frame_snaps = []
            orig_samples = self._samples[:]
            for i in range(1, len(orig_samples) + 1):
                self._samples = orig_samples[:i]
                self._update_graph(capture=True)
            self._samples = orig_samples
            self._update_graph()
        if len(self._frame_snaps) < 2:
            messagebox.showinfo("Not Enough Frames",
                                "Not enough data points to create animation.")
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
        hdrs = ["Sample", "Elapsed (s)", "Write Speed (MB/s)", "Bytes Written", "Capacity %", "Drive Total Bytes", "Notes"]

        dt    = self._drive_total
        notes = self._notes_var.get()

        if fmt == "csv":
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdrs)
                for row in rows:
                    w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                row[3], f"{row[4]:.2f}", dt, notes])
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
                    ws.write(ri, 5, self._drive_total)
                    ws.write(ri, 6, self._notes_var.get())
                wb.save(path)
            except ImportError:
                with open(path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(hdrs)
                    notes = self._notes_var.get()
                    dt = self._drive_total
                    for row in rows:
                        w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                    row[3], f"{row[4]:.2f}", dt, notes])
                messagebox.showinfo("Note",
                    "xlwt not installed — saved as CSV.\nInstall xlwt for true XLS.")
        else:
            notes = self._notes_var.get()
            dt = self._drive_total
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdrs)
                for row in rows:
                    w.writerow([row[0], f"{row[1]:.3f}", f"{row[2]:.2f}",
                                row[3], f"{row[4]:.2f}", dt, notes])
            messagebox.showinfo("Note",
                "Saved as CSV — open with Apple Numbers or rename to .csv.\n"
                "Full .numbers format requires macOS Numbers.")

        self._status_var.set(self._("data_saved").format(path=path))

    def _do_load_data(self):
        """Load a previously saved CSV and restore graph + stats."""
        path = filedialog.askopenfilename(
            title=self._("load_csv_title"),
            initialdir=_results_dir(),
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return

        samples = []
        drive_total_loaded = 0
        notes_loaded = ""
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    elapsed = float(row.get("Elapsed (s)", 0))
                    speed   = float(row.get("Write Speed (MB/s)", 0))
                    bw      = int(float(row.get("Bytes Written", 0)))
                    samples.append((elapsed, speed, bw))
                    if not drive_total_loaded:
                        try:
                            drive_total_loaded = int(float(row.get("Drive Total Bytes", 0)))
                        except Exception:
                            pass
                    if not notes_loaded:
                        notes_loaded = row.get("Notes", "")
        except Exception as e:
            messagebox.showerror("Load Failed", f"Could not read CSV:\n{e}")
            return

        if not samples:
            messagebox.showwarning("Empty File", self._("load_csv_invalid"))
            return

        self._samples      = samples
        self._target_bytes = max(s[2] for s in samples)
        # Use saved drive total for correct x-axis scaling
        self._drive_total  = drive_total_loaded if drive_total_loaded > 0 else self._target_bytes
        self._frame_snaps  = []
        # Reset plot objects so _update_graph does a clean full redraw
        self._plot_line = None
        self._plot_fill = None
        self._plot_peak = None
        self._plot_ax2  = None
        if notes_loaded:
            self._notes_var.set(notes_loaded)

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
            + ("<div class='notes'>" + self._notes_var.get().strip() + "</div>\n" if self._notes_var.get().strip() else "")
+             f"<div class='sub'>Generated by {APP_NAME} v{APP_VERSION}"
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
