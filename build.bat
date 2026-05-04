@echo off
setlocal

:: Extract exe name from spec file
for /f "tokens=2 delims='" %%a in ('findstr /i "name=" fill_the_pane.spec') do set EXE_NAME=%%a.exe

:: Extract version number
set VERSION=%EXE_NAME:Fill the Pane v=%
set VERSION=%VERSION:.exe=%
set PY_FILE=fill_the_pane_v%VERSION%.py

:: Run PyInstaller
python -m PyInstaller fill_the_pane.spec --noconfirm

if errorlevel 1 (
    echo BUILD FAILED.
    pause
    exit /b 1
)

:: Create latest\ folder if it doesn't exist
if not exist latest mkdir latest

:: Clear latest\ folder and copy latest .py
del /q "latest\*" 2>nul
copy "code\%PY_FILE%" "latest\%PY_FILE%"

:: Launch the exe
start "" "dist\%EXE_NAME%"

endlocal