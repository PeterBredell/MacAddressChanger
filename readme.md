# MAC Address Changer

This project is a tool designed to allow users to change the MAC address of their network interface cards (NICs). It provides a simple and efficient way to anonymize your network identity or troubleshoot network-related issues.

## Project Structure

```
MacAddressChanger/
├── bin/                  # Compiled executables
├── build/                # Build artifacts
├── docs/                 # Documentation
│   ├── cpp_setup.md      # C++ development setup guide
│   └── readme.md         # Original project documentation
├── scripts/              # Build and utility scripts
│   ├── build_cpp.bat     # CMake-based build script
│   ├── compile_cpp.bat   # Direct compilation script
│   └── test_compiler.bat # C++ compiler test script
├── src/                  # Source code
│   ├── cpp/              # C++ source files
│   │   └── macchanger.cpp # C++ implementation
│   └── python/           # Python source files
│       ├── macchanger.py  # Main Python implementation
│       └── setup_hyperv.py # Hyper-V setup utility
├── tools/                # Helper tools and utilities
├── .gitignore            # Git ignore file
├── CMakeLists.txt        # CMake build configuration
├── LICENSE               # Project license
└── README.md             # This file
```

## Features
- Change the MAC address of physical NICs.
- Restore the original MAC address when needed.
- User-friendly interface for seamless operation.
- Virtual NIC support for enhanced privacy (new).
- C++ implementation for better performance (in development).

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

### Python Version

1. Run the Python version directly:
   ```
   python src/python/macchanger.py
   ```

2. For Hyper-V setup (if needed):
   ```
   python src/python/setup_hyperv.py
   ```

### C++ Version

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
We aim to expand the functionality of this project by incorporating the following features:
- **Enhanced Virtual NIC Support**:
  - Improved tunneling of network traffic through virtual NICs.
  - Better integration with Hyper-V and other virtualization platforms.
- **Complete C++ Implementation**: Finishing the C++ version with all features of the Python version.
- **Packaged GUI Version**: A user-friendly graphical interface will be introduced for easier operation.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the [MIT License](LICENSE).
