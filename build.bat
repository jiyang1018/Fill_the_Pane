@echo on
setlocal

:: ── Build Fill the Pane ──────────────────────────────────────────────────────
:: Reads the version from fill_the_pane.spec, builds the exe,
:: copies it to latest\, then launches it.

:: Extract version from spec file (looks for: name='Fill the Pane vX.X.XX')
for /f "tokens=2 delims='" %%a in ('findstr /i "name=" fill_the_pane.spec') do set EXE_NAME=%%a.exe

echo.
echo Building %EXE_NAME%...
echo.

:: Run PyInstaller
python -m PyInstaller fill_the_pane.spec --noconfirm

if errorlevel 1 (
    echo.
    echo BUILD FAILED.
    cmd /k
)

:: Create latest\ folder if it doesn't exist
if not exist latest mkdir latest

:: Clear latest\ folder
del /q "latest\*" 2>nul

:: Copy new exe to latest\
copy "dist\%EXE_NAME%" "latest\%EXE_NAME%"

echo.
echo Build complete: %EXE_NAME%
echo Copied to latest\
echo.

:: Launch the exe
start "" "dist\%EXE_NAME%"

echo.
echo Done.
cmd /k