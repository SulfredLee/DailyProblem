cmake_minimum_required (VERSION 3.8.2)

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project(SFLib)

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

include("/home/sulfred/Documents/cppEnv/DCEnv/vcpkg/scripts/buildsystems/vcpkg.cmake")
# Handle QT
if (UNIX)
else ()
  # Handle QT on windows
  set(QT_ROOT "C:\\Qt\\5.6.2\\5.6\\msvc2013_64\\")
  set(QT_INCLUDE_DIR "${QT_ROOT}include")
  set(QT_LIBRARY_DIR "${QT_ROOT}lib")
  set(CMAKE_PREFIX_PATH ${QT_ROOT})
endif ()
# Handle QT libraries
find_package(
  Qt5
  REQUIRED Core Gui Widgets
  )
message(STATUS "Info - QT library status:")
message(STATUS "Info -     version: ${Qt5Widgets_VERSION}")
message(STATUS "Info -     libraries: ${Qt5Widgets_LIBRARIES} ${Qt5Core_LIBRARIES} ${Qt5Core_QTMAIN_LIBRARIES} ${Qt5Gui_LIBRARIES}")
message(STATUS "Info -     include path: ${Qt5Widgets_INCLUDE_DIRS}")

# Handle GTest
find_package(GTest CONFIG REQUIRED)
message(STATUS "Gtest include: " ${GTEST_INCLUDE_DIRS})

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(app)
add_subdirectory(lib)
# add_subdirectory(test)

