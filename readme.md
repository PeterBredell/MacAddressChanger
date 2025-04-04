# MAC Address Changer

This project is a tool designed to allow users to change the MAC address of their network interface cards (NICs). It provides a simple and efficient way to anonymize your network identity or troubleshoot network-related issues.

> **Note:** This tool is designed for educational and legitimate network troubleshooting purposes only. Users are responsible for ensuring they comply with all applicable network policies, terms of service, and laws when using this tool.

## Project Structure

```
MacAddressChanger/
├── bin/                  # Compiled executables
├── build/                # Build artifacts
├── docs/                 # Documentation
│   ├── README.md         # Documentation overview
│   ├── cpp_setup.md      # C++ development setup guide
│   └── readme.md         # Original project documentation
├── launchers/            # Quick-start launcher scripts
│   ├── README.md         # Launchers overview
│   ├── run_macchanger.bat     # Launch Python version
│   ├── run_macchanger_cpp.bat # Launch C++ version
│   └── setup_hyperv.bat       # Launch Hyper-V setup
├── scripts/              # Build and utility scripts
│   ├── README.md         # Scripts overview
│   ├── build_cpp.bat     # CMake-based build script
│   ├── compile_cpp.bat   # Direct compilation script
│   └── test_compiler.bat # C++ compiler test script
├── src/                  # Source code
│   ├── README.md         # Source code overview
│   ├── cpp/              # C++ source files
│   │   └── macchanger.cpp # C++ implementation
│   └── python/           # Python source files
│       ├── macchanger.py  # Main Python implementation
│       └── setup_hyperv.py # Hyper-V setup utility
├── tools/                # Helper tools and utilities
│   ├── README.md         # Tools overview
│   ├── check_environment.bat # Environment verification
│   └── clean_build.bat       # Clean build artifacts
├── .gitignore            # Git ignore file
├── CMakeLists.txt        # CMake build configuration
├── LICENSE               # Project license
└── README.md             # This file
```

## Features
- Change the MAC address of physical NICs
- Restore the original MAC address when needed
- User-friendly command-line interface for seamless operation
- Virtual NIC support for enhanced privacy and bypassing MAC filtering
- Hyper-V integration for advanced virtualization scenarios
- Cross-language implementation (Python and C++)

## Current Status

- **Python Version**: Fully functional with all core features implemented
- **C++ Version**: Basic implementation in progress
- **Hyper-V Support**: Initial implementation complete
- **Project Structure**: Organized for maintainability and future development

## Requirements
- Operating System: Windows
- Administrator privileges for modifying network configurations.
- For C++ version: MSYS2 with MinGW-w64 (see docs/cpp_setup.md)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/PeterBredell/MacAddressChanger.git
    ```
2. Navigate to the project directory:
    ```bash
    cd MacAddressChanger
    ```

## Usage

### Using Launcher Scripts

The easiest way to use the application is with the launcher scripts in the `launchers` directory:

1. For the Python version:
   ```
   launchers\run_macchanger.bat
   ```

2. For the C++ version:
   ```
   launchers\run_macchanger_cpp.bat
   ```

3. For Hyper-V setup (if needed):
   ```
   launchers\setup_hyperv.bat
   ```

### Manual Execution

#### Python Version

1. Run the Python version directly:
   ```
   python src/python/macchanger.py
   ```

2. For Hyper-V setup (if needed):
   ```
   python src/python/setup_hyperv.py
   ```

#### C++ Version

1. Build the C++ version:
   ```
   scripts/build_cpp.bat
   ```

   Or compile directly:
   ```
   scripts/compile_cpp.bat
   ```

2. Run the compiled executable:
   ```
   bin/macchanger_cpp.exe
   ```

## Development

For C++ development setup instructions, see [docs/cpp_setup.md](docs/cpp_setup.md).

## Future Plans

We aim to expand the functionality of this project with the following goals:

### Short-term Goals (Next 3 Months)
- **Complete C++ Implementation**:
  - Implement all features from the Python version in C++
  - Optimize performance for faster MAC address operations
  - Ensure compatibility with the latest Windows versions

### Medium-term Goals (3-6 Months)
- **Enhanced Virtual NIC Support**:
  - Improve tunneling of network traffic through virtual NICs
  - Add support for custom network configurations
  - Implement better error handling and recovery mechanisms
- **Expanded Hyper-V Integration**:
  - Add support for more advanced Hyper-V networking scenarios
  - Implement MAC address rotation for virtual machines
  - Create templates for common virtualization setups

### Long-term Goals (6+ Months)
- **Graphical User Interface**:
  - Develop a user-friendly GUI for easier operation
  - Create a system tray application for quick MAC changes
  - Add scheduling capabilities for automatic MAC rotation
- **Cross-Platform Support**:
  - Extend functionality to Linux and macOS
  - Create a unified codebase that works across platforms
  - Implement platform-specific optimizations

### Ongoing Improvements
- **Code Quality**: Continuous refactoring and optimization
- **Documentation**: Improve and expand documentation
- **Testing**: Implement comprehensive test suite
- **Security**: Regular security audits and improvements

## Compatibility and Known Issues

### Compatibility
- **Windows Versions**: Tested on Windows 10 and Windows 11
- **Network Adapters**: Works with most physical and virtual network adapters
- **Administrator Rights**: Required for all MAC address operations

### Known Issues
- Some network adapters may not support MAC address changes
- Certain security software may block MAC address modifications
- Virtual NIC creation requires Hyper-V to be enabled
- MAC address changes may temporarily disconnect network interfaces

## Contributing

Contributions are welcome! Here's how you can contribute to the project:

1. **Report Issues**: Submit bugs and feature requests through GitHub Issues
2. **Suggest Improvements**: Share your ideas for making the tool better
3. **Submit Pull Requests**: Implement new features or fix bugs
4. **Improve Documentation**: Help make the documentation more comprehensive
5. **Test on Different Systems**: Verify compatibility across different environments

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This tool is provided for educational and legitimate network troubleshooting purposes only. The authors are not responsible for any misuse or damage caused by this tool. Always ensure you have permission to modify network settings on the systems you use this tool with.
