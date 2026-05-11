@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo  Fill the Pane -- build ftp_loop.dll
echo ====================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "CPP_FILE=%SCRIPT_DIR%ftp_loop.cpp"
set "DLL_FILE=%SCRIPT_DIR%ftp_loop.dll"
set "LOG_FILE=%SCRIPT_DIR%build_dll.log"

if not exist "%CPP_FILE%" (
    echo ERROR: ftp_loop.cpp not found in %SCRIPT_DIR%
    echo Make sure build_dll.bat and ftp_loop.cpp are in the same folder.
    goto :fail
)

:: ---- Check for MSVC cl.exe in PATH ----
echo [1/3] Looking for MSVC cl.exe...
where cl.exe >nul 2>&1
if %errorlevel% == 0 (
    echo       Found cl.exe in PATH.
    goto :build_msvc
)

:: Try common Visual Studio locations
for %%V in (
    "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
    "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat"
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
) do (
    if exist %%V (
        echo       Found Visual Studio, loading environment...
        call %%V >nul 2>&1
        goto :build_msvc
    )
)
echo       MSVC not found.

:: ---- Check for MinGW g++ in PATH ----
echo [1/3] Looking for MinGW g++...
where g++ >nul 2>&1
if %errorlevel% == 0 (
    echo       Found g++ in PATH.
    goto :build_mingw
)

:: Try common MinGW locations
if exist "C:\msys64\mingw64\bin\g++.exe" (
    set "GPP=C:\msys64\mingw64\bin\g++.exe"
    goto :build_mingw_direct
)
if exist "C:\msys64\ucrt64\bin\g++.exe" (
    set "GPP=C:\msys64\ucrt64\bin\g++.exe"
    goto :build_mingw_direct
)
if exist "C:\mingw64\bin\g++.exe" (
    set "GPP=C:\mingw64\bin\g++.exe"
    goto :build_mingw_direct
)
if exist "C:\mingw\bin\g++.exe" (
    set "GPP=C:\mingw\bin\g++.exe"
    goto :build_mingw_direct
)
if exist "C:\TDM-GCC-64\bin\g++.exe" (
    set "GPP=C:\TDM-GCC-64\bin\g++.exe"
    goto :build_mingw_direct
)
echo       MinGW not found.

:: ---- Try winget to install MSYS2 ----
echo.
echo [2/3] No compiler found. Trying to install MinGW via winget...
echo       This is a one-time download (~50 MB). Please wait.
echo.

where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: winget not available.
    goto :manual
)

winget install --id MSYS2.MSYS2 --silent --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    echo ERROR: winget install failed.
    goto :manual
)

echo       Installing mingw-w64 toolchain...
"C:\msys64\usr\bin\bash.exe" -lc "pacman -S --noconfirm mingw-w64-x86_64-gcc" >nul 2>&1

if exist "C:\msys64\mingw64\bin\g++.exe" (
    set "GPP=C:\msys64\mingw64\bin\g++.exe"
    echo       MinGW installed OK.
    goto :build_mingw_direct
)

echo ERROR: Install appeared to succeed but g++ not found.
goto :manual

:: ---- Build with MSVC ----
:build_msvc
echo.
echo [2/3] Compiling with MSVC...
cl /O2 /LD /EHsc /W3 "%CPP_FILE%" /Fe:"%DLL_FILE%" /link kernel32.lib >"%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Compile failed. See build_dll.log for details.
    type "%LOG_FILE%"
    goto :fail
)
goto :verify

:: ---- Build with MinGW (g++ in PATH) ----
:build_mingw
echo.
echo [2/3] Compiling with MinGW g++...
:: Resolve full path to g++ and prepend its bin dir so all MinGW
:: runtime DLLs (libisl, libmpc, libgmp, libgcc_s_seh etc.) are found.
for /f "delims=" %%P in ('where g++') do set "GPP_FULL=%%P" & goto :mingw_path_set
:mingw_path_set
for %%F in ("%GPP_FULL%") do set "PATH=%%~dpF;%PATH%"
g++ -O2 -shared -o "%DLL_FILE%" "%CPP_FILE%" -lkernel32 -static-libgcc -static-libstdc++ >"%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Compile failed. See build_dll.log for details.
    type "%LOG_FILE%"
    goto :fail
)
goto :verify

:: ---- Build with MinGW (full path to g++) ----
:build_mingw_direct
echo.
echo [2/3] Compiling with MinGW g++ at %GPP%...
:: Prepend the MinGW bin dir to PATH so libisl-23.dll and other
:: toolchain DLLs are found when g++.exe runs.
for %%F in ("%GPP%") do set "MINGW_BIN=%%~dpF"
set "PATH=%MINGW_BIN%;%PATH%"
"%GPP%" -O2 -shared -o "%DLL_FILE%" "%CPP_FILE%" -lkernel32 -static-libgcc -static-libstdc++ >"%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Compile failed. See build_dll.log for details.
    type "%LOG_FILE%"
    goto :fail
)
goto :verify

:: ---- Verify ----
:verify
echo.
if not exist "%DLL_FILE%" (
    echo ERROR: ftp_loop.dll was not created.
    goto :fail
)
echo [3/3] Done.
echo.
echo       ftp_loop.dll created successfully.
echo.
echo ====================================================
echo  SUCCESS. Now run build.bat to build the exe.
echo ====================================================
goto :end

:: ---- Manual instructions ----
:manual
echo.
echo ====================================================
echo  Auto-install failed. Manual steps:
echo ====================================================
echo.
echo  1. Go to this URL in your browser:
echo     https://github.com/niXman/mingw-builds-binaries/releases
echo.
echo  2. Download the file named:
echo     x86_64-XX.X.X-release-win32-seh-msvcrt-rt_vXX-revX.7z
echo     (pick the latest version)
echo.
echo  3. Extract it so that g++.exe ends up at:
echo     C:\mingw64\bin\g++.exe
echo.
echo  4. Re-run this script.
echo.
goto :fail

:fail
echo.
echo Build FAILED.
pause
exit /b 1

:end
pause
exit /b 0
