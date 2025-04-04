@echo off
echo Checking development environment...

REM Navigate to project root directory
cd ..

echo.
echo === Python Environment ===
python --version
echo.

echo === C++ Environment ===
where g++ 2>nul
if %ERRORLEVEL% EQU 0 (
    echo g++ found in PATH:
    g++ --version
) else (
    echo g++ not found in PATH. Please install MinGW-w64 or check your PATH settings.
    echo See docs/cpp_setup.md for installation instructions.
)

echo.
echo === Build Tools ===
where cmake 2>nul
if %ERRORLEVEL% EQU 0 (
    echo CMake found:
    cmake --version
) else (
    echo CMake not found. Please install CMake or check your PATH settings.
)

echo.
echo === Project Structure ===
echo Checking for required directories...
set MISSING=0

if not exist "src\cpp" (
    echo MISSING: src\cpp directory
    set MISSING=1
)

if not exist "src\python" (
    echo MISSING: src\python directory
    set MISSING=1
)

if not exist "bin" (
    echo MISSING: bin directory
    set MISSING=1
)

if not exist "docs" (
    echo MISSING: docs directory
    set MISSING=1
)

if not exist "scripts" (
    echo MISSING: scripts directory
    set MISSING=1
)

if %MISSING% EQU 0 (
    echo All required directories are present.
)

echo.
echo Environment check complete.
pause
