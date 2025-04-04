@echo off
echo Building C++ project...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

REM Navigate to project root directory
cd ..

REM Check if build directory exists, if not create it
if not exist "build" mkdir build
cd build

REM Run CMake to generate build files
"C:\msys64\ucrt64\bin\cmake.exe" .. -G "MinGW Makefiles"

REM Build the project
"C:\msys64\ucrt64\bin\mingw32-make.exe"

REM Create bin directory if it doesn't exist
if not exist "bin" mkdir bin

REM Copy the executable to the bin directory
if exist "bin\macchanger_cpp.exe" copy bin\macchanger_cpp.exe ..

cd ..
echo Build complete. Executable is in the bin directory.
pause
