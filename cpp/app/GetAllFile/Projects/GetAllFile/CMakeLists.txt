cmake_minimum_required (VERSION 3.8.2)

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project(GetAllFile)

# Turn on the ability to create folders to organize projects (.vcproj)
# It creates "CMakePredefinedTargets" folder by default and adds CMake
# defined projects like INSTALL.vcproj and ZERO_CHECK.vcproj
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Command to output information to the console
# Useful for displaying errors, warnings, and debugging
set(CMAKE_CXX_FLAGS "-Wall -fPIC -std=c++2a -g")
message(STATUS "Root - cxx Flags: " ${CMAKE_CXX_FLAGS})

# Handle Preprocess Flags
if (UNIX)
  add_definitions(-DUNIX)
  find_package(
    Threads
  ) # include pthread in linux enviroment
else ()
  add_definitions(-DWINDOWS -DWIN32 "/EHsc")
endif ()
message(STATUS "Info - CMAKE_THREAD_LIBS_INIT: ${CMAKE_THREAD_LIBS_INIT}")

# include("~/Documents/cppEnv/DCEnv/vcpkg/scripts/buildsystems/vcpkg.cmake")

# Handle GTest
find_package(GTest CONFIG REQUIRED)
message(STATUS "Gtest include: " ${GTEST_INCLUDE_DIRS})

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(app)
# add_subdirectory(lib)
# add_subdirectory(test)

