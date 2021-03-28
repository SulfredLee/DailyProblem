#!/bin/bash

function PrepareRootCMakeFile {
    local outputFile=$1

    echo "cmake_minimum_required (VERSION 3.8.2)

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)
include (ExternalProject)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project(${projectName})

# Turn on the ability to create folders to organize projects (.vcproj)
# It creates \"CMakePredefinedTargets\" folder by default and adds CMake
# defined projects like INSTALL.vcproj and ZERO_CHECK.vcproj
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Command to output information to the console
# Useful for displaying errors, warnings, and debugging
set(CMAKE_CXX_FLAGS \"-Wall -fPIC -std=c++2a -g\")
message(STATUS \"Root - cxx Flags: \" \${CMAKE_CXX_FLAGS})

# Add External Project
include (${projectName}.cmake)

# Handle dependencies
# ExternalProject_Add_StepDependencies(${projectName} build
#   ProjectB
#   )
" > ${outputFile}
}

function PrepareMainProjectCMakeFile {
    local outputFile=$1

    echo "cmake_minimum_required (VERSION 3.8.2)

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)

# Maps to a solution filed (*.sln). The solution will
# have all targets (exe, lib, dll) as projects (.vcproj)
project(${projectName})

# Turn on the ability to create folders to organize projects (.vcproj)
# It creates \"CMakePredefinedTargets\" folder by default and adds CMake
# defined projects like INSTALL.vcproj and ZERO_CHECK.vcproj
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Command to output information to the console
# Useful for displaying errors, warnings, and debugging
set(CMAKE_CXX_FLAGS \"-Wall -fPIC -std=c++2a -g\")
message(STATUS \"Root - cxx Flags: \" \${CMAKE_CXX_FLAGS})

# Handle Preprocess Flags
if (UNIX)
  add_definitions(-DUNIX)
  find_package(
    Threads
  ) # include pthread in linux enviroment
else ()
  add_definitions(-DWINDOWS -DWIN32 \"/EHsc\")
endif ()
message(STATUS \"Info - CMAKE_THREAD_LIBS_INIT: ${CMAKE_THREAD_LIBS_INIT}\")

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(app)
add_subdirectory(lib)
" > ${outputFile}
}

function PrepareReadmeFile {
    local buildType=$1
    local outputFile=$2

    echo "# Usage:
cmake -G Ninja ../Projects -DCMAKE_BUILD_TYPE=${buildType} -DCMAKE_INSTALL_PREFIX=../Install -DCMAKE_TOOLCHAIN_FILE=../Projects/vcpkg/scripts/buildsystems/vcpkg.cmake
ninja

About vcpkg https://docs.microsoft.com/en-us/cpp/build/install-vcpkg?view=msvc-160&tabs=linux:
# Install vcpkg
git clone https://github.com/microsoft/vcpkg
./bootstrap-vcpkg.sh

# Manage package
./vcpkg list
./vcpkg search | grep json
./vcpkg install xxx

Before run you may need to locate those libraries
export LD_LIBRARY_PATH=../Install/lib" > ${outputFile}
}

function PrepareExternalCMakeFile {
    local projectType=$1
    local projectName=$2
    local outputFile=$3

    echo "include (ExternalProject)

# Add External ${projectName}
set (${projectName} \"${projectName}\")
ExternalProject_Add (
  \${${projectName}}

  PREFIX Projects/\${${projectName}}
" > ${outputFile}

    if [[ "Git" == ${projectType} ]]; then
        echo "
  GIT_REPOSITORY https://github.com/taglib/taglib
  GIT_TAG        v1.11.1
  GIT_SHALLOW    ON
" >> ${outputFile}
    elif [[ "Local" == ${projectType} ]]; then
        echo "  SOURCE_DIR \${PROJECT_SOURCE_DIR}/\${${projectName}}
" >> ${outputFile}
    fi

    echo "  BUILD_ALWAYS   ON
  INSTALL_DIR    \${CMAKE_INSTALL_PREFIX}

  CMAKE_CACHE_ARGS
  -DBUILD_SHARED_LIBS:BOOL=ON
  -DENABLE_STATIC_RUNTIME:BOOL=OFF
  -DBUILD_EXAMPLES:BOOL=ON
  -DCMAKE_BUILD_TYPE:STRING=\${CMAKE_BUILD_TYPE}
  -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>

  BUILD_COMMAND \${CMAKE_COMMAND} --build <BINARY_DIR>
  )
" >> ${outputFile}
}
function PrepareMainProject {
    local projectName=$1
    echo "Prepare project: ${projectName}"

    local debugPath="./${projectName}/Debug"
    local releasePath="./${projectName}/Release"
    local installPath="./${projectName}/Install"
    local projectsPath="./${projectName}/Projects"
    local mainProjectPath="./${projectName}/Projects/${projectName}"

    # Prepare directories
    mkdir -p ${debugPath}
    mkdir -p ${releasePath}
    mkdir -p ${installPath}
    mkdir -p ${projectsPath}
    mkdir -p ${mainProjectPath}/app
    mkdir -p ${mainProjectPath}/lib
    mkdir -p ${mainProjectPath}/test

    # Prepare files
    PrepareRootCMakeFile ${projectsPath}/CMakeLists.txt
    PrepareExternalCMakeFile "Local" ${projectName} ${projectsPath}/${projectName}.cmake
    PrepareMainProjectCMakeFile ${mainProjectPath}/CMakeLists.txt
    PrepareReadmeFile "Debug" ${debugPath}/readme.txt
    PrepareReadmeFile "Release" ${releasePath}/readme.txt
}

function PrepareApp {
    local appName=$1
    echo "Prepare app: ${appName}"

    mkdir -p ./${appName}

    # app root CMake file
    grep -qxF "add_subdirectory(${appName})" CMakeLists.txt || echo "add_subdirectory(${appName})" >> CMakeLists.txt
    # app CMake file
    echo "set(targetName \"${appName}\")
get_filename_component(folderName \${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE \" \" \"_\" folderName \${folderName})

set(CMAKE_CXX_FLAGS \"\${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations\")

file(GLOB \${folderName}_inc
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.h\")
file(GLOB \${folderName}_src
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")

include_directories(
  \${CMAKE_CURRENT_SOURCE_DIR}
  )
  # \${PROJECT_SOURCE_DIR}/../ProjectB/lib/PrintHelper
  # \${PROJECT_SOURCE_DIR}/lib/utility
  # \${libpng_INCLUDE_DIR}
  # \${libbmp_INCLUDE_DIR})

add_executable(\${targetName} \${\${folderName}_src})

# target_link_libraries(
#   \${targetName}
#   \${CMAKE_INSTALL_PREFIX}/lib/libPrintHelper.so
#   \${CMAKE_THREAD_LIBS_INIT}
#   utility
#   \${libpng_LIBRARY_DIR}/libpng16.so
#   \${libbmp_LIBRARY_DIR}/libbmp.so)

# Creates a folder \"executables\" and adds target
# project (*.vcproj) under it
set_property(TARGET \${targetName} PROPERTY FOLDER \"executables\")

# Adds logic to INSTALL.vcproj to copy *.exe to destination directory
install (TARGETS \${targetName} DESTINATION bin)" > ./${appName}/CMakeLists.txt
    # app main file
    echo "#include <iostream>

int main (int argc, char *argv[])
{
    return 0;
}" > ./${appName}/main.cpp
}

function PrepareLib {
    local libType=$1
    local libName=$2

    echo "Prepare ${libType} library: ${libName}"
    mkdir -p ./${libName}

    # lib root CMake file
    grep -qxF "add_subdirectory(${libName})" CMakeLists.txt || echo "add_subdirectory(${libName})" >> CMakeLists.txt
    # lib CMake file
    echo "set(targetName \"${libName}\")
get_filename_component(folderName \${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE \" \" \"_\" folderName \${folderName})

file(GLOB \${folderName}_inc
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.h\")
file(GLOB \${folderName}_src
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")

include_directories(
  \${CMAKE_CURRENT_SOURCE_DIR}
  # \${Boost_INCLUDE_DIR}
  )

# state that this project is a library" > ./${libName}/CMakeLists.txt
    if [[ "static" == ${libType} ]]; then
        echo "add_library(\${targetName} STATIC \${\${folderName}_src}) # static library" >> ./${libName}/CMakeLists.txt
    else
        echo "add_library(\${targetName} SHARED \${\${folderName}_src}) # dynamic library" >> ./${libName}/CMakeLists.txt
    fi

    echo "
if (UNIX)
#   target_link_libraries(
#     \${targetName}
#     \${CMAKE_THREAD_LIBS_INIT}
#     )
else ()
endif ()

# Creates a folder \"libraries\" and adds target project (*.vcproj) under it
set_property(TARGET \${targetName} PROPERTY FOLDER \"libraries\")

# Adds logic to INSTALL.vcproj to copy *.a to destination directory
install (TARGETS \${targetName} DESTINATION lib)
install (FILES \${\${folderName}_inc} DESTINATION include)" >> ./${libName}/CMakeLists.txt
}

# Main
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 --[project|static_library|dynamic_library|app_name] (name)"
    exit
fi

POSITIONAL=()
EXTERNAL_PROJECT_NAME=""
MAIN_PROJECT_NAME=""
STATIC_LIBRARY=""
DYNAMIC_LIBRARY=""
APP_NAME=""
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -p|--main_project)
            MAIN_PROJECT_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        -e|--external_project)
            EXTERNAL_PROJECT_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        -s|--static_library)
            STATIC_LIBRARY="$2"
            shift # past argument
            shift # past value
            ;;
        -d|--dynamic_library)
            DYNAMIC_LIBRARY="$2"
            shift # past argument
            shift # past value
            ;;
        -a|--app_name)
            APP_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        --default)
            DEFAULT=YES
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ ${MAIN_PROJECT_NAME} != "" ]]; then
    PrepareMainProject ${MAIN_PROJECT_NAME}
elif [[ ${EXTERNAL_PROJECT_NAME} != "" ]]; then
    PrepareExternalCMakeFile "Git" ${EXTERNAL_PROJECT_NAME} ./${EXTERNAL_PROJECT_NAME}.cmake
elif [[ ${STATIC_LIBRARY} != "" ]]; then
    PrepareLib "static" ${STATIC_LIBRARY}
elif [[ ${DYNAMIC_LIBRARY} != "" ]]; then
    PrepareLib "dynamic" ${DYNAMIC_LIBRARY}
elif [[ ${APP_NAME} != "" ]]; then
    PrepareApp ${APP_NAME}
fi
