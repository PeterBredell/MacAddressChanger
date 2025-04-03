@echo off
echo Testing C++ compiler setup...

REM Set PATH to include MinGW binaries
SET PATH=%PATH%;C:\msys64\ucrt64\bin

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
echo #include ^<iostream^> > test.cpp
echo int main() { std::cout ^<^< "Compiler test successful!" ^<^< std::endl; return 0; } >> test.cpp

"C:\msys64\ucrt64\bin\g++.exe" -o test.exe test.cpp

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful. Running test program:
    test.exe
    del test.cpp test.exe
) else (
    echo Compilation failed with error code %ERRORLEVEL%
)

echo.
echo Test complete.
pause
