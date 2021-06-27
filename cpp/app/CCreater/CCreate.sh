#!/bin/bash

function PrepareRootCMakeFile {
    local outputFile=$1
    local appPath=$2

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
include (${appPath}/YourProject.cmake)

# Handle dependencies
# ExternalProject_Add_StepDependencies(${projectName} build
#   ProjectB
#   )
" > ${outputFile}
}

function PrepareHunterCommonCMakeFile {
    local outputFolder=$1
    local outputFile=${outputFolder}/hunterCommon.cmake

    echo "# Copyright (c) 2013, 2015 Ruslan Baratov
# All rights reserved.

cmake_minimum_required(VERSION 3.0)

### Include HunterGate module from git submodule
set(gate_dir \"\${CMAKE_CURRENT_LIST_DIR}/../gate\")
set(gate_module \"\${gate_dir}/cmake/HunterGate.cmake\")

get_filename_component(gate_module \"\${gate_module}\" ABSOLUTE)
if(NOT EXISTS \"\${gate_module}\")
  message(
      FATAL_ERROR
      \"\${gate_module} module not found (update git submodule needed?)\"
  )
endif()

message(\"Including HunterGate: \${gate_module}\")
include(\"\${gate_module}\")

### Check testing variables are set
string(COMPARE EQUAL \"\${TESTING_URL}\" \"\" url_is_empty)
string(COMPARE EQUAL \"\${TESTING_SHA1}\" \"\" sha1_is_empty)
string(COMPARE EQUAL \"\${HUNTER_ROOT}\" \"\" hunter_root_is_empty)

if(NOT url_is_empty AND NOT sha1_is_empty AND NOT hunter_root_is_empty)
  get_filename_component(TESTING_URL \"\${TESTING_URL}\" ABSOLUTE)

  ### HunterGate module
  HunterGate(URL \"\${TESTING_URL}\" SHA1 \"\${TESTING_SHA1}\" \${TESTING_CONFIG_OPT})
else()
  get_filename_component(HUNTER_ROOT \"\${CMAKE_CURRENT_LIST_DIR}/..\" ABSOLUTE)
  HunterGate(URL \"x\" SHA1 \"xxxxxxxx\" \${TESTING_CONFIG_OPT})
endif()" > ${outputFile}

}

function PrepareMainProjectCMakeFile {
    local outputFile=$1
    local qtEnable=$2
    local projectName=$3
    local srcFolder=$4

    # PrepareHunterCommonCMakeFile ${projectName}

    echo "cmake_minimum_required (VERSION 3.8.2)

# Prepare Package manager
# look for GTestTargets.cmake under ~/.hunter for more information about usefule variable
include (\"cmake/HunterGate.cmake\")

# Usable variables can be found from files <package>-config.cmake
# look for set_target_properties()
# set(CMAKE_HOST_SYSTEM_PROCESSOR \"x86_64\")
# include (\"./vcpkg/scripts/buildsystems/vcpkg.cmake\")

# build a CPack driven installer package
include (InstallRequiredSystemLibraries)
include (CPack)

HunterGate (
  URL \"https://github.com/cpp-pm/hunter/archive/v0.23.304.tar.gz\"
  SHA1 \"cae9026e69d7d8333897663688a11f4232fb8826\"
)

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
message(STATUS \"Info - CMAKE_THREAD_LIBS_INIT: \${CMAKE_THREAD_LIBS_INIT}\")
" > ${outputFile}

    if [[ "Y" == ${qtEnable} ]]; then
        echo "
# Handle QT
if (UNIX)
else ()
  # Handle QT on windows
  set(QT_ROOT \"C:\\\\Qt\\\\5.6.2\\\\5.6\\\\msvc2013_64\\\\\")
  set(QT_INCLUDE_DIR \"\${QT_ROOT}include\")
  set(QT_LIBRARY_DIR \"\${QT_ROOT}lib\")
  set(CMAKE_PREFIX_PATH \${QT_ROOT})
endif ()
# Handle QT libraries
find_package(
  Qt5
  REQUIRED Core Gui Widgets
  )
message(STATUS \"Info - QT library status:\")
message(STATUS \"Info -     version: \${Qt5Widgets_VERSION}\")
message(STATUS \"Info -     libraries: \${Qt5Widgets_LIBRARIES} \${Qt5Core_LIBRARIES} \${Qt5Core_QTMAIN_LIBRARIES} \${Qt5Gui_LIBRARIES}\")
message(STATUS \"Info -     include path: \${Qt5Widgets_INCLUDE_DIRS}\")
" >> ${outputFile}
    fi

    echo "
# Handle GTest
hunter_add_package(GTest)
find_package(GTest CONFIG REQUIRED)
get_target_property(GTEST_INCLUDE_DIRS GTest::gtest INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS \"Gtest include: \" \${GTEST_INCLUDE_DIRS})

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(${srcFolder})
# add_subdirectory(lib)
add_subdirectory(test)
" >> ${outputFile}
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

    echo "PrepareExternalCMakeFile projectType: ${projectType} projectName: ${projectName} outputFile: ${outputFile}"
    echo "include (ExternalProject)

# Add External ${projectName}
set (thisProject \"${projectName}\")
ExternalProject_Add (
  \${thisProject}

  PREFIX Projects/\${thisProject}
" > ${outputFile}

    if [[ "Git" == ${projectType} ]]; then
        echo "
  GIT_REPOSITORY https://github.com/taglib/taglib
  GIT_TAG        v1.11.1
  GIT_SHALLOW    ON
" >> ${outputFile}
    elif [[ "Local" == ${projectType} ]]; then
        echo "  SOURCE_DIR \${CMAKE_CURRENT_LIST_DIR}/\${thisProject}
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
  -DCMAKE_TOOLCHAIN_FILE:FILE=\${CMAKE_TOOLCHAIN_FILE}

  BUILD_COMMAND \${CMAKE_COMMAND} --build <BINARY_DIR>
  )
" >> ${outputFile}
}

function PrepareTestCMakeFile {
    local projectName=test_${1}
    local outputFile=$2

    echo "set(targetName \"${projectName}\")
get_filename_component(folderName \${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE \" \" \"_\" folderName \${folderName})

set(CMAKE_CXX_FLAGS \"\${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations\")

file(GLOB ${folderName}_inc
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.h\")
file(GLOB \${folderName}_src
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")

include_directories(
  \${CMAKE_CURRENT_SOURCE_DIR}
  \${PROJECT_SOURCE_DIR}/src
  \${GTEST_INCLUDE_DIRS}
  )
  # \${PROJECT_SOURCE_DIR}/../ProjectB/lib/PrintHelper
  # \${PROJECT_SOURCE_DIR}/lib/utility
  # \${libpng_INCLUDE_DIR}
  # \${libbmp_INCLUDE_DIR})

add_executable(\${targetName} \${\${folderName}_src})

target_link_libraries(
  \${targetName}
  GTest::gmock GTest::gtest GTest::gmock_main GTest::gtest_main
  ${projectName}
  )
#   \${CMAKE_INSTALL_PREFIX}/lib/libPrintHelper.so
#   \${CMAKE_THREAD_LIBS_INIT}
#   utility
#   \${libpng_LIBRARY_DIR}/libpng16.so
#   \${libbmp_LIBRARY_DIR}/libbmp.so)

add_test(NAME \${targetName} COMMAND \${targetName})
if (\${CMAKE_BUILD_TYPE} STREQUAL \"Debug\")
  add_custom_command(
    TARGET \${targetName}
    POST_BUILD
    COMMAND \${targetName}
    )
endif()

# Creates a folder \"executables\" and adds target
# project (*.vcproj) under it
set_property(TARGET \${targetName} PROPERTY FOLDER \"executables\")

# Adds logic to INSTALL.vcproj to copy *.exe to destination directory
install (TARGETS \${targetName} DESTINATION bin)
" > ${outputFile}
}

function PrepareTestMainFile {
    local outputFile=$1

    echo "#include \"gtest/gtest.h\"
#include \"gmock/gmock.h\"

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    int ret = RUN_ALL_TESTS();
    return ret;
}
" > ${outputFile}
}

function PrepareTestClassFile {
    local projectName=${2}
    local outputHeaderFile=${1}/Test${projectName}.h
    local outputSrcFile=${1}/Test${projectName}.cpp

    echo "#ifndef TEST_${projectName}_H
#define TEST_${projectName}_H
#include \"gtest/gtest.h\"
#include \"gmock/gmock.h\"

class Test${projectName} : public testing::Test
{
 public:
    virtual void SetUp() {}
    virtual void TearDown() {}
};

#endif
" > ${outputHeaderFile}

    echo "#include \"Test${projectName}.h\"

/*
EXPECT_EQ(val1,val2);, val1 == val2
EXPECT_NE(val1,val2);, val1 != val2
EXPECT_LT(val1,val2);, val1 < val2
EXPECT_LE(val1,val2);, val1 <= val2
EXPECT_GT(val1,val2);, val1 > val2
EXPECT_GE(val1,val2);, val1 >= val2
*/

TEST_F(Test${projectName}, Test001)
{
    EXPECT_EQ(true, true);
}
" > ${outputSrcFile}

}

function PrepareTestDirectory {
    local projectName=${1}
    local outputFolder=${projectName}/test

    PrepareTestCMakeFile ${projectName} ${outputFolder}/CMakeLists.txt
    PrepareTestMainFile ${outputFolder}/main.cpp
    PrepareTestClassFile ${outputFolder} ${projectName}
}

function PrepareCCMakeFile {
    local projectsPath=$1
    local makeFileName=$2
    local outputFile=${projectsPath}/${makeFileName}

    echo "
function PrepareRunBuildFile {
    local buildType=\$1
    local outputFile=\$2

    echo \"#!/bin/bash
    # example folder: /home/<user>/Documents/cppEnv/DCEnv/vcpkg/scripts/buildsystems/vcpkg.cmake
    toolChainFolder=\\\$1
    if [[ -z \\\${toolChainFolder} ]]; then
        cmake -G Ninja ../ -DCMAKE_BUILD_TYPE=\${buildType} -DCMAKE_INSTALL_PREFIX=../install
    else
        cmake -G Ninja ../ -DCMAKE_BUILD_TYPE=\${buildType} -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_TOOLCHAIN_FILE=\\\${toolChainFolder}/vcpkg/scripts/buildsystems/vcpkg.cmake
    fi
    \" > \${outputFile}

    chmod +x \${outputFile}
}

function PrepareDebugBuild {
    local folderPath=\"debug\"

    echo \"Prepare Debug Folder\"

    mkdir \${folderPath}
    mkdir -p install
    PrepareRunBuildFile \"Debug\" \${folderPath}/\"CCMake.sh\"
}

function PrepareReleaseBuild {
    local folderPath=\"release\"

    echo \"Prepare Release Folder\"

    mkdir \${folderPath}
    mkdir -p install
    PrepareRunBuildFile \"release\" \${folderPath}/\"CCMake.sh\"
}

POSITIONAL=()
BUILD_TYPE=\"\"
while [[ \$# -gt 0 ]]
do
    key=\"\$1\"

    case \$key in
        -t|--build_type)
            BUILD_TYPE=\"\$2\"
            shift # past argument
            shift # past value
            ;;
        --default)
            DEFAULT=YES
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=(\"\$1\") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- \"\${POSITIONAL[@]}\" # restore positional parameters

if [[ \${BUILD_TYPE} == \"debug\" ]]; then
    PrepareDebugBuild
elif [[ \${BUILD_TYPE} == \"release\" ]]; then
    PrepareReleaseBuild
elif [[ \${BUILD_TYPE} == \"\" ]]; then
    PrepareDebugBuild
    PrepareReleaseBuild
fi
" > ${outputFile}

    chmod +x ${outputFile}
}

function PrepareMainProject {
    local projectName=$1
    local qtEnable=$2
    echo "Prepare project: ${projectName} qtEnable: ${qtEnable}"

    # Prepare directories
    mkdir -p ${projectName}/app
    mkdir -p ${projectName}/lib

    # Prepare files
    PrepareRootCMakeFile ${projectName}/CMakeLists.txt "app"
    PrepareCCMakeFile ${projectName} "CCMake.sh"
    PrepareReadmeFile "Debug" ${projectName}/readme.txt
}

function PrepareAppMainFile {
    local appName=$1
    local qtEnable=$2
    local outputPath=$3

    if [[ "Y" == ${qtEnable} ]]; then
        echo "#include <iostream>
#include <QApplication>
#include \"mainwindow.h\"

int main (int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow MW;
    MW.show();
    bool bRTN = app.exec();

    return bRTN;
}" > ./${outputPath}/main.cpp
    else
        echo "#include <iostream>

int main (int argc, char *argv[])
{
    std::cout << \"Hello World\" << std::endl;
    return 0;
}" > ./${outputPath}/main.cpp
    fi
}

function PrepareAppCMakeFile {
    local appName=$1
    local qtEnable=$2
    local outputPath=$3

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
#   \${libbmp_LIBRARY_DIR}/libbmp.so
#   \${Qt5Core_LIBRARIES}
#   \${Qt5Core_QTMAIN_LIBRARIES}
#   \${Qt5Gui_LIBRARIES}
#   \${Qt5Widgets_LIBRARIES}
#   )

# Creates a folder \"executables\" and adds target
# project (*.vcproj) under it
set_property(TARGET \${targetName} PROPERTY FOLDER \"executables\")

# Adds logic to INSTALL.vcproj to copy *.exe to destination directory
install (TARGETS \${targetName} DESTINATION bin)" > ./${outputPath}/CMakeLists.txt
}

function DownloadHunter {
    local workPath=$1

    mkdir ${workPath}/cmake
    wget https://raw.githubusercontent.com/cpp-pm/gate/master/cmake/HunterGate.cmake -O ${workPath}/cmake/HunterGate.cmake
}

function PrepareVCPKGFile {
    local workPath=$1
    local outputFile=${workPath}/Preparevcpkg.sh

    echo "git clone https://github.com/microsoft/vcpkg
cd ./vcpkg
./bootstrap-vcpkg.sh" > ${outputFile}

    chmod +x ${outputFile}
}

function PrepareApp {
    local appName=$1
    local qtEnable=$2
    echo "Prepare app: ${appName} qtEnable: ${qtEnable}"

    mkdir -p ./${appName}
    mkdir -p ./${appName}/app
    mkdir -p ./${appName}/lib
    mkdir -p ./${appName}/test

    PrepareExternalCMakeFile "Local" ${appName} ${appName}.cmake
    PrepareMainProjectCMakeFile ${appName}/CMakeLists.txt ${qtEnable} ${appName} "app"
    DownloadHunter ${appName}
    PrepareVCPKGFile ${appName}
    PrepareAppCMakeFile ${appName} ${qtEnable} ${appName}/app
    PrepareAppMainFile ${appName} ${qtEnable} ${appName}/app
    PrepareTestDirectory ${appName}
}

function PrepareLibNonQT {
    local libType=$1
    local libName=$2
    local outputPath=$3

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

# state that this project is a library" > ./${outputPath}/CMakeLists.txt
    if [[ "static" == ${libType} ]]; then
        echo "add_library(\${targetName} STATIC \${\${folderName}_src}) # static library" >> ./${outputPath}/CMakeLists.txt
    else
        echo "add_library(\${targetName} SHARED \${\${folderName}_src}) # dynamic library" >> ./${outputPath}/CMakeLists.txt
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
install (FILES \${\${folderName}_inc} DESTINATION include)" >> ./${outputPath}/CMakeLists.txt
}

function PrepareLibQT {
    local libType=$1
    local libName=$2
    local outputPath=$3

    echo "set(targetName \"${libName}\")
get_filename_component(folderName \${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE \" \" \"_\" folderName \${folderName})

# Handle QT libraries
file(GLOB \${folderName}_src \"\${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")
file(GLOB \${folderName}_hdr \"\${CMAKE_CURRENT_SOURCE_DIR}/*.h\")
file(GLOB \${folderName}_ui \"\${CMAKE_CURRENT_SOURCE_DIR}/*.ui\")
# set(\${folderName}_rcc \${CMAKE_CURRENT_SOURCE_DIR}/resource.qrc)
qt5_wrap_cpp(\${folderName}_hdr_moc \${\${folderName}_hdr})
# qt5_wrap_ui (\${folderName}_ui_moc  \${\${folderName}_src} \${\${folderName}_ui})
qt5_wrap_ui (\${folderName}_ui_moc  \${\${folderName}_ui})
# qt5_add_resources(\${folderName}_rcc_moc \${\${folderName}_rcc})

# handle other resource
# file(GLOB PlayerEngine_inc
#   \"\${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine/*.h\")
# file(GLOB PlayerEngine_src
#   \"\${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine/*.cpp\")

include_directories(
  \${QT_INCLUDE_DIR}
  \${QT_INCLUDE_DIR}/QtWidgets
  \${CMAKE_CURRENT_SOURCE_DIR}
  \${PROJECT_BINARY_DIR}/lib/\${folderName}
  # \${libpcap_INCLUDE_DIR}
  # \${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine
  )

if (UNIX)
  # handle library files for installation
  file(GLOB libqt_libFile \"\${QT_LIBRARY_DIR}/*so*\")
else ()
endif ()

message(STATUS \"qt include: \" \${QT_INCLUDE_DIR})
message(STATUS \"binary folder: \" \${PROJECT_BINARY_DIR}/\${folderName})
message(STATUS \"cmake current dir: \" \${CMAKE_CURRENT_SOURCE_DIR})
message(STATUS \"source file: \" \${\${folderName}_ui_moc})" > ./${outputPath}/CMakeLists.txt

    if [[ "static" == ${libType} ]]; then
        echo "add_library(
  \${targetName} STATIC
  \${\${folderName}_src}
  \${\${folderName}_hdr}
  \${\${folderName}_hdr_moc}
  \${\${folderName}_ui_moc}
  # \${\${folderName}_rcc_moc}
  # \${PlayerEngine_src}
  ) # static library" >> ./${outputPath}/CMakeLists.txt
    else
        echo "add_library(
  \${targetName} SHARED
  \${\${folderName}_src}
  \${\${folderName}_hdr}
  \${\${folderName}_hdr_moc}
  \${\${folderName}_ui_moc}
  # \${\${folderName}_rcc_moc}
  # \${PlayerEngine_src}
  ) # dynamic library" >> ./${outputPath}/CMakeLists.txt
    fi

    echo "
target_link_libraries(
  \${targetName}
  \${Qt5Widgets_LIBRARIES}
  )

# Creates a folder \"libraries\" and adds target project (*.vcproj) under it
set_property(TARGET \${targetName} PROPERTY FOLDER \"libraries\")

# Adds logic to INSTALL.vcproj to copy *.lib to destination directory
install (TARGETS \${targetName} DESTINATION lib)
install (FILES \${\${folderName}_hdr_proxy} DESTINATION include)
install (FILES \${libqt_libFile} DESTINATION lib)
" >> ./${outputPath}/CMakeLists.txt
}

function PrepareLib {
    local libType=$1
    local libName=$2
    local qtEnable=$3

    echo "Prepare ${libType} library: ${libName} qtEnable: ${qtEnable}"
    mkdir -p ./${libName}
    mkdir -p ./${libName}/src
    mkdir -p ./${libName}/test

    # lib root CMake file
    grep -qxF "add_subdirectory(${libName})" CMakeLists.txt || echo "add_subdirectory(${libName})" >> CMakeLists.txt

    echo "add_subdirectory(src)" > ./${libName}/CMakeLists.txt
    echo "add_subdirectory(test)" >> ./${libName}/CMakeLists.txt

    PrepareTestDirectory ${libName}
    if [[ "Y" == ${qtEnable} ]]; then
        PrepareLibQT ${libType} ${libName} ${libName}/src
    else
        PrepareLibNonQT ${libType} ${libName} ${libName}/src
    fi
}

function PrepareLibProject {
    local libType=$1
    local libName=$2
    local qtEnable=$3

    echo "Prepare ${libType} library: ${libName} qtEnable: ${qtEnable}"
    mkdir -p ./${libName}
    mkdir -p ./${libName}/src
    mkdir -p ./${libName}/test

    PrepareExternalCMakeFile "Local" ${libName} ${libName}.cmake
    PrepareMainProjectCMakeFile ${libName}/CMakeLists.txt ${qtEnable} ${libName} "src"
    DownloadHunter ${libName}
    PrepareVCPKGFile ${libName}
    PrepareTestDirectory ${libName}
    if [[ "Y" == ${qtEnable} ]]; then
        PrepareLibQT ${libType} ${libName} ${libName}/src
    else
        PrepareLibNonQT ${libType} ${libName} ${libName}/src
    fi
}

function PrepareTest {
    local testName=$1
    local h_file="${testName}Test.h"
    local cpp_file="${testName}Test.cpp"
    local upperCaseName=${testName^^}

    echo "#ifndef ${upperCaseName}_TEST_H
#define ${upperCaseName}_TEST_H

#include \"gtest/gtest.h\"

class ${testName}Test : public ::testing::Test {

 protected:

    // You can do set-up work for each test here.
    ${testName}Test() {}

    // You can do clean-up work that doesn't throw exceptions here.
    virtual ~${testName}Test() {}

    // If the constructor and destructor are not enough for setting up
    // and cleaning up each test, you can define the following methods:

    // Code here will be called immediately after the constructor (right
    // before each test).
    virtual void SetUp() {}

    // Code here will be called immediately after each test (right
    // before the destructor).
    virtual void TearDown() {}
};

#endif
" > ${h_file}

    echo "#include \"${testName}Test.h\"

TEST_F(${testName}Test, Test001)
{
    EXPECT_EQ(true, true);
}
" > ${cpp_file}

}

function PrintHelp {
    echo "Usage:"
    echo "# Create main project"
    echo "\$ $0 --main_project <YourProjectName>"
    echo "\$ $0 --main_project <YourProjectName> --qt_enable"
    echo "\$ $0 --main_project <YourProjectName> --vcpkg_path <ThePath>"

    echo ""
    echo "# Create app"
    echo "\$ cd ./<YourProjectName>/app"
    echo "\$ $0 --app_project <YourApp>"
    echo "\$ $0 --app_project <YourApp> --qt_enable"

    echo ""
    echo "# Create static library project"
    echo "\$ cd ./<YourProjectName>/lib"
    echo "\$ $0 --static_library_project <YourLibName>"
    echo "\$ $0 --static_library_project <YourLibName> --qt_enable"

    echo ""
    echo "# Create dynamic library project"
    echo "\$ cd ./<YourProjectName>/lib"
    echo "\$ $0 --dynamic_library_project <YourLibName>"
    echo "\$ $0 --dynamic_library_project <YourLibName> --qt_enable"

    echo ""
    echo "# Create static library"
    echo "\$ cd ./<YourProjectName>/lib"
    echo "\$ $0 --static_library <YourLibName>"
    echo "\$ $0 --static_library <YourLibName> --qt_enable"

    echo ""
    echo "# Create dynamic library"
    echo "\$ cd ./<YourProjectName>/lib"
    echo "\$ $0 --dynamic_library <YourLibName>"
    echo "\$ $0 --dynamic_library <YourLibName> --qt_enable"

    echo ""
    echo "# Create test sub project"
    echo "\$ cd ./<YourProjectName/test"
    echo "\$ $0 --test_name <TestName>"
}

# Main
if (( "$#" < 2 )); then
    PrintHelp
    exit
fi

POSITIONAL=()
EXTERNAL_PROJECT_NAME=""
LOCAL_PROJECT_NAME=""
MAIN_PROJECT_NAME=""
STATIC_LIBRARY_PROJECT=""
DYNAMIC_LIBRARY_PROJECT=""
STATIC_LIBRARY=""
DYNAMIC_LIBRARY=""
APP_PROJECT=""
TEST_NAME=""
QT_ENABLE="N"
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -h|--help)
            PrintHelp
            shift # past argument
            ;;
        -p|--main_project)
            MAIN_PROJECT_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        -q|--qt_enable)
            QT_ENABLE="Y"
            shift # past argument
            ;;
        -e|--external_project)
            EXTERNAL_PROJECT_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        -l|--local_project)
            LOCAL_PROJECT_NAME="$2"
            shift # past argument
            shift # past value
            ;;
        -sp|--static_library_project)
            STATIC_LIBRARY_PROJECT="$2"
            shift # past argument
            shift # past value
            ;;
        -dp|--dynamic_library_project)
            DYNAMIC_LIBRARY_PROJECT="$2"
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
        -a|--app_project)
            APP_PROJECT="$2"
            shift # past argument
            shift # past value
            ;;
        -t|--test_name)
            TEST_NAME="$2"
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
    PrepareMainProject ${MAIN_PROJECT_NAME} ${QT_ENABLE}
elif [[ ${EXTERNAL_PROJECT_NAME} != "" ]]; then
    PrepareExternalCMakeFile "Git" ${EXTERNAL_PROJECT_NAME} ./${EXTERNAL_PROJECT_NAME}.cmake
elif [[ ${LOCAL_PROJECT_NAME} != "" ]]; then
    PrepareExternalCMakeFile "Local" ${LOCAL_PROJECT_NAME} ./${LOCAL_PROJECT_NAME}.cmake
elif [[ ${STATIC_LIBRARY_PROJECT} != "" ]]; then
    PrepareLibProject "static" ${STATIC_LIBRARY_PROJECT} ${QT_ENABLE}
elif [[ ${DYNAMIC_LIBRARY_PROJECT} != "" ]]; then
    PrepareLibProject "dynamic" ${DYNAMIC_LIBRARY_PROJECT} ${QT_ENABLE}
elif [[ ${STATIC_LIBRARY} != "" ]]; then
    PrepareLib "static" ${STATIC_LIBRARY} ${QT_ENABLE}
elif [[ ${DYNAMIC_LIBRARY} != "" ]]; then
    PrepareLib "dynamic" ${DYNAMIC_LIBRARY} ${QT_ENABLE}
elif [[ ${APP_PROJECT} != "" ]]; then
    PrepareApp ${APP_PROJECT} ${QT_ENABLE}
elif [[ ${TEST_NAME} != "" ]]; then
    PrepareTest ${TEST_NAME}
fi
