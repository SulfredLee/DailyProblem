cmake_minimum_required (VERSION 3.8.2)

# Prepare Package manager
# look for GTestTargets.cmake under ~/.hunter for more information about usefule variable
include ("cmake/HunterGate.cmake")

# Usable variables can be found from files <package>-config.cmake
# look for set_target_properties()
# set(CMAKE_HOST_SYSTEM_PROCESSOR "x86_64")
# include ("./vcpkg/scripts/buildsystems/vcpkg.cmake")

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)

HunterGate (
  URL "https://github.com/cpp-pm/hunter/archive/v0.23.304.tar.gz"
  SHA1 "cae9026e69d7d8333897663688a11f4232fb8826"
)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project(QuickFixDataCtrl)

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


# Handle GTest
hunter_add_package(GTest)
find_package(GTest CONFIG REQUIRED)
get_target_property(GTEST_INCLUDE_DIRS GTest::gtest INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "Gtest include: " ${GTEST_INCLUDE_DIRS})

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(src)
# add_subdirectory(lib)
add_subdirectory(test)

