# fill_the_pane.spec  —  PyInstaller spec for single-file portable exe
#
# Usage:
#   pip install pyinstaller matplotlib psutil pillow
#   pyinstaller fill_the_pane.spec
#
# Output:  dist\Fill the Pane vX.X.XX.exe

block_cipher = None

a = Analysis(
    ['latest/fill_the_pane_v0.5.41.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_agg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'matplotlib.animation',
        'matplotlib.ticker',
        'psutil',
        'PIL',
        'PIL.Image',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'csv',
        'shutil',
        'webbrowser',
        'ctypes',
        'ctypes.wintypes',
        'configparser',
        'math',
        'json',
        'platform',
        'matplotlib.ft2font',
        'matplotlib.backends._backend_tk',
        'matplotlib.backends.backend_tkagg',
        'matplotlib._path',
        'matplotlib.textpath',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Fill the Pane v0.5.41',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True,
)
