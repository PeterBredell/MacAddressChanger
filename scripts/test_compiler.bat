@echo off
echo Testing C++ compiler setup...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

REM Navigate to project root directory
cd ..

echo.
echo Checking g++ version:
"C:\msys64\ucrt64\bin\g++.exe" --version

echo.
echo Checking if g++ is in PATH:
where g++

echo.
echo Checking if cmake is available:
"C:\msys64\ucrt64\bin\cmake.exe" --version

echo.
echo Checking if make is available:
"C:\msys64\ucrt64\bin\mingw32-make.exe" --version

echo.
echo Testing simple compilation:
echo #include ^<iostream^> > tools\test.cpp
echo int main() { std::cout ^<^< "Compiler test successful!" ^<^< std::endl; return 0; } >> tools\test.cpp

"C:\msys64\ucrt64\bin\g++.exe" -o tools\test.exe tools\test.cpp

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful. Running test program:
    tools\test.exe
    del tools\test.cpp tools\test.exe
) else (
    echo Compilation failed with error code %ERRORLEVEL%
)

echo.
echo Test complete.
pause
