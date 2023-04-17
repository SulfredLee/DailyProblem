content_st = """
cmake_minimum_required (VERSION 3.8.2)

# Usable variables can be found from files <package>-config.cmake
# look for set_target_properties()
# set(CMAKE_HOST_SYSTEM_PROCESSOR "x86_64")
# include ("./vcpkg/scripts/buildsystems/vcpkg.cmake")

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)
include (ExternalProject)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project({{ project_name }})

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
find_package(GTest CONFIG REQUIRED)
get_target_property(GTEST_INCLUDE_DIRS GTest::gtest INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "Gtest include: " ${GTEST_INCLUDE_DIRS})

# Handle libpqxx --- c++ library for postgresql connection
# use this after ./vcpkg install libpqxx
# https://www.tutorialspoint.com/postgresql/postgresql_c_cpp.htm
# find_package(libpqxx CONFIG REQUIRED)
# message(STATUS "libpqxx include: " ${libpqxx_INCLUDE_DIRS})
# message(STATUS "libpqxx libraries: " ${libpqxx_LIBRARY_DIR})

# Handle boost
# https://cmake.org/cmake/help/latest/module/FindBoost.html
# use this after ./vcpkg install boost-thread
# XXXXX you no need to use find package for all boost libraries, for example lockfree is the exception
# find_package(Boost REQUIRED thread)
# message(STATUS "Boost include: " ${Boost_INCLUDE_DIRS})
# message(STATUS "Boost libraries: " ${Boost_LIBRARIES})

# Handle atomic-queue
# https://github.com/max0x7ba/atomic_queue
# use this after ./vcpkg install atomic-queue
# find_path(ATOMIC_QUEUE_INCLUDE_DIRS "atomic_queue/atomic_queue.h")
# message(STATUS "atomic-queue include: " ${ATOMIC_QUEUE_INCLUDE_DIRS})

# Add third party library

# Add subdirectory
add_subdirectory(app)
add_subdirectory(test)

# Add External Project
"""
