# C++ Development Setup for MacAddressChanger

This guide explains how to set up a C++ development environment for the MacAddressChanger project.

## Prerequisites

- Windows 10 or newer (64-bit)
- Administrator privileges for installation
- Visual Studio Code (recommended)

## Installation Steps

### 1. Install MSYS2

1. Download the MSYS2 installer from: [https://github.com/msys2/msys2-installer/releases/download/2025-02-21/msys2-x86_64-20250221.exe](https://github.com/msys2/msys2-installer/releases/download/2025-02-21/msys2-x86_64-20250221.exe)
2. Run the installer and follow the installation steps
3. Choose a simple installation path (avoid spaces and special characters)
4. When the installation completes, the MSYS2 terminal will open

### 2. Install Required Packages

1. In the MSYS2 terminal (UCRT64), update the package database:
   ```
   pacman -Syu
   ```
   (You may need to close and reopen the terminal if prompted)

2. Install the GCC compiler and related tools:
   ```
   pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-make mingw-w64-ucrt-x86_64-cmake
   ```

### 3. Add MinGW-w64 to PATH

1. Open Windows Settings > System > About > Advanced system settings
2. Click on "Environment Variables"
3. Under "System variables", find the "Path" variable and click "Edit"
4. Click "New" and add the path to the MinGW-w64 bin directory:
   ```
   C:\msys64\ucrt64\bin
   ```
   (Adjust the path if you installed MSYS2 to a different location)
5. Click "OK" to close all dialogs

### 4. Test Your Setup

1. Open Command Prompt or PowerShell
2. Verify that the compiler is available:
   ```
   g++ --version
   ```
3. You should see the GCC version information

## Visual Studio Code Setup

### 1. Install Required Extensions

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Install the following extensions:
   - C/C++ (Microsoft)
   - C/C++ Extension Pack (Microsoft)
   - CMake Tools (Microsoft)

### 2. Configure VS Code

The project already includes the following configuration files in the `.vscode` folder:

- `c_cpp_properties.json`: Configures IntelliSense
- `tasks.json`: Defines build tasks
- `launch.json`: Configures debugging
- `settings.json`: Sets VS Code settings for C++ development

If VS Code doesn't recognize the g++ compiler, try these steps:

1. Restart VS Code after adding MinGW to your PATH
2. Open a new terminal in VS Code (Terminal > New Terminal)
3. Verify the compiler is available in the VS Code terminal:
   ```
   g++ --version
   ```
4. If it's still not recognized, try using the full path in commands:
   ```
   C:\msys64\ucrt64\bin\g++.exe --version
   ```

## Building the C++ Project

### Using the Batch Files

Two batch files are provided for building:

1. `build_cpp.bat`: Uses CMake and Make to build the project
   ```
   build_cpp.bat
   ```

2. `compile_cpp.bat`: Directly compiles macchanger.cpp without CMake
   ```
   compile_cpp.bat
   ```

### Using VS Code Tasks

1. Open VS Code
2. Press Ctrl+Shift+B to see available build tasks
3. Select "Build C++ Project" to build using CMake
4. Or select "Compile Current File" to compile the currently open file

### Manual Build

If you prefer to build manually:

1. Create a build directory:
   ```
   mkdir build
   cd build
   ```

2. Generate build files with CMake:
   ```
   "C:\msys64\ucrt64\bin\cmake.exe" .. -G "MinGW Makefiles"
   ```

3. Build the project:
   ```
   "C:\msys64\ucrt64\bin\mingw32-make.exe"
   ```

4. The executable will be created in the build directory

## Troubleshooting

### Common Issues

1. **"g++ not recognized" in VS Code**
   - Make sure you've added MinGW to your PATH
   - Restart VS Code completely
   - Try using the full path to g++ in your commands
   - Check if the `.vscode/settings.json` file has the correct paths

2. **CMake not found**
   - Verify that you installed the cmake package in MSYS2
   - Try using the full path to cmake.exe

3. **IntelliSense not working**
   - Make sure the C/C++ extension is installed
   - Check that the paths in `.vscode/c_cpp_properties.json` are correct
   - Reload the window (Ctrl+Shift+P, then "Developer: Reload Window")

4. **Build fails**
   - Check the error messages for specific issues
   - Verify that all required packages are installed
   - Try the direct compilation method with `compile_cpp.bat`

### Additional Resources

- MSYS2 documentation: https://www.msys2.org/docs/
- MinGW-w64 documentation: https://www.mingw-w64.org/
- VS Code C++ documentation: https://code.visualstudio.com/docs/languages/cpp
