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
# The flag: -D_GLIBCXX_DEBUG is useful for dangling iterator detection
# The flag: -fprofile-arcs -ftest-coverage is useful for gcov and lcov
# The flag: -pg is used for activating the gprof profiling
# The flag: -D_GLIBCXX_DEBUG is used for dangling dereference checking
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -fPIC -std=c++2a")
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g3 -D_GLIBCXX_DEBUG -fprofile-arcs -ftest-coverage -pg -D_GLIBCXX_DEBUG")
message(STATUS "Root - cxx Flags: " ${CMAKE_CXX_FLAGS})
message(STATUS "Root - cxx Flags Release: " ${CMAKE_CXX_FLAGS_RELEASE})
message(STATUS "Root - cxx Flags Debug: " ${CMAKE_CXX_FLAGS_DEBUG})

message(STATUS "Root - CMAKE_C_FLAGS_DEBUG is ${CMAKE_C_FLAGS_DEBUG}")
message(STATUS "Root - CMAKE_C_FLAGS_RELEASE is ${CMAKE_C_FLAGS_RELEASE}")
message(STATUS "Root - CMAKE_C_FLAGS_RELWITHDEBINFO is ${CMAKE_C_FLAGS_RELWITHDEBINFO}")
message(STATUS "Root - CMAKE_C_FLAGS_MINSIZEREL is ${CMAKE_C_FLAGS_MINSIZEREL}")
message(STATUS "")
message(STATUS "Root - CMAKE_CXX_FLAGS_DEBUG is ${CMAKE_CXX_FLAGS_DEBUG}")
message(STATUS "Root - CMAKE_CXX_FLAGS_RELEASE is ${CMAKE_CXX_FLAGS_RELEASE}")
message(STATUS "Root - CMAKE_CXX_FLAGS_RELWITHDEBINFO is ${CMAKE_CXX_FLAGS_RELWITHDEBINFO}")
message(STATUS "Root - CMAKE_CXX_FLAGS_MINSIZEREL is ${CMAKE_CXX_FLAGS_MINSIZEREL}")
message(STATUS "Root - CMAKE_CXX_FLAGS is " ${CMAKE_CXX_FLAGS})
message(STATUS "")
message(STATUS "Root - CMAKE_BUILD_TYPE is " ${CMAKE_BUILD_TYPE})
message(STATUS "")

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

# Handle google benchmark
find_package(benchmark CONFIG REQUIRED)
# target_link_libraries(main PRIVATE benchmark::benchmark benchmark::benchmark_main)

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
# add_subdirectory(test)
# add_subdirectory(user_benchmark)

# Add External Project
"""
