@echo off
setlocal

:: Extract exe name from spec file
for /f "tokens=2 delims='" %%a in ('findstr /i "name=" fill_the_pane.spec') do set EXE_NAME=%%a.exe

:: Extract version number
set VERSION=%EXE_NAME:Fill the Pane v=%
set VERSION=%VERSION:.exe=%
set PY_FILE=fill_the_pane_v%VERSION%.py

:: Verify source exists in latest\
if not exist "latest\%PY_FILE%" (
    echo ERROR: latest\%PY_FILE% not found.
    echo Place the source file in latest\ before building.
    pause
    exit /b 1
)

:: Copy current version from latest\ to code\ for history
if not exist code mkdir code
copy "latest\%PY_FILE%" "code\%PY_FILE%" >nul

:: Clear latest\ and keep only the current version
for %%f in (latest\*.py) do (
    if /i not "%%f"=="latest\%PY_FILE%" del "%%f"
)

:: Run PyInstaller
python -m PyInstaller fill_the_pane.spec --noconfirm

if errorlevel 1 (
    echo BUILD FAILED.
    pause
    exit /b 1
)

:: Launch the exe
start "" "dist\%EXE_NAME%"

endlocal