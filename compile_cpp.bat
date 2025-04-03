@echo off
echo Compiling macchanger.cpp directly...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

REM Compile the C++ file
"C:\msys64\ucrt64\bin\g++.exe" -o macchanger_cpp.exe macchanger.cpp

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful. Executable is macchanger_cpp.exe
) else (
    echo Compilation failed with error code %ERRORLEVEL%
)

pause
