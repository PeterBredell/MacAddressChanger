@echo off
echo Cleaning build artifacts...

REM Navigate to project root directory
cd ..

REM Remove build directory contents
if exist "build" (
    echo Removing build directory contents...
    rd /s /q build
    mkdir build
)

REM Clean bin directory (but keep directory structure)
if exist "bin" (
    echo Cleaning bin directory...
    del /q bin\*.*
)

echo Build artifacts cleaned successfully.
pause
