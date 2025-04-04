@echo off
echo Compiling macchanger.cpp directly...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

REM Navigate to project root directory
cd ..

REM Create bin directory if it doesn't exist
if not exist "bin" mkdir bin

REM Compile the C++ file
"C:\msys64\ucrt64\bin\g++.exe" -o bin\macchanger_cpp.exe src\cpp\macchanger.cpp

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful. Executable is in the bin directory.
) else (
    echo Compilation failed with error code %ERRORLEVEL%
)

pause
