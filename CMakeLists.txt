cmake_minimum_required(VERSION 3.10)
project(MacAddressChanger VERSION 1.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/src/cpp)

# Add executable
add_executable(macchanger_cpp src/cpp/macchanger.cpp)

# Set output directory
set_target_properties(macchanger_cpp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

# Install target
install(TARGETS macchanger_cpp DESTINATION bin)
