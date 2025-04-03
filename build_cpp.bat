@echo off
echo Building C++ project...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

REM Check if build directory exists, if not create it
if not exist "build" mkdir build
cd build

REM Run CMake to generate build files
"C:\msys64\ucrt64\bin\cmake.exe" .. -G "MinGW Makefiles"

REM Build the project
"C:\msys64\ucrt64\bin\mingw32-make.exe"

REM Copy the executable to the main directory
copy macchanger_cpp.exe ..

cd ..
echo Build complete. Executable is macchanger_cpp.exe
pause
