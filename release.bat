@echo off
setlocal

:: Extract version from spec file
for /f "tokens=2 delims='" %%a in ('findstr /i "name=" fill_the_pane.spec') do set EXE_NAME=%%a
set VERSION=%EXE_NAME:Fill the Pane v=%

echo.
echo Releasing Fill the Pane v%VERSION%...
echo.

:: Pull latest entry from changelog.md and prepend to CHANGELOG.md
python prepend_changelog.py %VERSION%
if %errorlevel% neq 0 (
    echo ERROR: prepend_changelog.py failed. Aborting release.
    pause
    exit /b 1
)

:: Stage all changes (source, changelog, spec, dll, readme etc.)
git add .

:: Commit
git commit -m "v%VERSION%"

:: Push code
git push

:: Delete old tag if exists (ignore errors if tag does not exist)
git tag -d v%VERSION% 2>nul
git push origin --delete v%VERSION% 2>nul

:: Create and push new tag to trigger release workflow
git tag v%VERSION%
git push origin v%VERSION%

echo.
echo Done. Check https://github.com/jiyang1018/Fill_the_Pane/actions for build status.
echo.
pause
endlocal
