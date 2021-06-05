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
    local qtEnable=$2
    local vcpkgPath=$3

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
message(STATUS \"Info - CMAKE_THREAD_LIBS_INIT: \${CMAKE_THREAD_LIBS_INIT}\")

include(\"${vcpkgPath}/vcpkg/scripts/buildsystems/vcpkg.cmake\")" > ${outputFile}

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
find_package(GTest CONFIG REQUIRED)
message(STATUS \"Gtest include: \" \${GTEST_INCLUDE_DIRS})

# Sub-directories where more CMakeLists.txt exist
add_subdirectory(app)
# add_subdirectory(lib)
# add_subdirectory(test)
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
        echo "  SOURCE_DIR \${PROJECT_SOURCE_DIR}/\${thisProject}
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
    local outputFile=$1

    echo "set(targetName \"unitTest\")
get_filename_component(folderName \${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE \" \" \"_\" folderName \${folderName})

set(CMAKE_CXX_FLAGS \"\${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations\")

file(GLOB ${folderName}_inc
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.h\")
file(GLOB \${folderName}_src
  \"\${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")

include_directories(
  \${CMAKE_CURRENT_SOURCE_DIR}
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

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    int ret = RUN_ALL_TESTS();
    return ret;
}
" > ${outputFile}
}

function PrepareTestDirectory {
    local outputFolder=$1

    PrepareTestCMakeFile ${outputFolder}/CMakeLists.txt
    PrepareTestMainFile ${outputFolder}/main.cpp
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
    local vcpkgPath=$3
    echo "Prepare project: ${projectName} qtEnable: ${qtEnable} vcpkgPath: ${vcpkgPath}"

    local projectsPath="./${projectName}"
    local mainProjectPath="./${projectName}/${projectName}"

    # Prepare directories
    mkdir -p ${mainProjectPath}/app
    mkdir -p ${mainProjectPath}/lib
    mkdir -p ${mainProjectPath}/test

    # Prepare files
    PrepareRootCMakeFile ${projectsPath}/CMakeLists.txt
    PrepareExternalCMakeFile "Local" ${projectName} ${projectsPath}/${projectName}.cmake
    PrepareMainProjectCMakeFile ${mainProjectPath}/CMakeLists.txt ${qtEnable} ${vcpkgPath}
    PrepareTestDirectory ${mainProjectPath}/test
    PrepareCCMakeFile ${projectsPath} "CCMake.sh"
    PrepareReadmeFile "Debug" ${mainProjectPath}/readme.txt
}

function PrepareApp {
    local appName=$1
    local qtEnable=$2
    echo "Prepare app: ${appName} qtEnable: ${qtEnable}"

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
install (TARGETS \${targetName} DESTINATION bin)" > ./${appName}/CMakeLists.txt
    # app main file
    if [[ "Y" == ${qtEnable} ]]; then
        echo "#include <iostream>

int main (int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow MW;
    MW.show();
    bool bRTN = app.exec();

    return bRTN;
}" > ./${appName}/main.cpp
    else
        echo "#include <iostream>

int main (int argc, char *argv[])
{
    std::cout << \"Hello World\" << std::endl;
    return 0;
}" > ./${appName}/main.cpp
    fi
}

function PrepareLibNonQT {
    local libType=$1
    local libName=$2

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

function PrepareLibQT {
    local libType=$1
    local libName=$2

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
message(STATUS \"source file: \" \${\${folderName}_ui_moc})" > ./${libName}/CMakeLists.txt

    if [[ "static" == ${libType} ]]; then
        echo "add_library(
  \${targetName} STATIC
  \${\${folderName}_src}
  \${\${folderName}_hdr}
  \${\${folderName}_hdr_moc}
  \${\${folderName}_ui_moc}
  # \${\${folderName}_rcc_moc}
  # \${PlayerEngine_src}
  ) # static library" >> ./${libName}/CMakeLists.txt
    else
        echo "add_library(
  \${targetName} SHARED
  \${\${folderName}_src}
  \${\${folderName}_hdr}
  \${\${folderName}_hdr_moc}
  \${\${folderName}_ui_moc}
  # \${\${folderName}_rcc_moc}
  # \${PlayerEngine_src}
  ) # dynamic library" >> ./${libName}/CMakeLists.txt
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
" >> ./${libName}/CMakeLists.txt
}

function PrepareLib {
    local libType=$1
    local libName=$2
    local qtEnable=$3

    echo "Prepare ${libType} library: ${libName} qtEnable: ${qtEnable}"
    mkdir -p ./${libName}

    # lib root CMake file
    grep -qxF "add_subdirectory(${libName})" CMakeLists.txt || echo "add_subdirectory(${libName})" >> CMakeLists.txt

    if [[ "Y" == ${qtEnable} ]]; then
        PrepareLibQT ${libType} ${libName}
    else
        PrepareLibNonQT ${libType} ${libName}
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

    echo ""
    echo "# Create app"
    echo "\$ cd ./<YourProjectName>/app"
    echo "\$ $0 --app_name <YourApp>"
    echo "\$ $0 --app_name <YourApp> --qt_enable"
    echo "\$ $0 --app_name <YourApp> --vcpkg_path <ThePath>"

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
STATIC_LIBRARY=""
DYNAMIC_LIBRARY=""
APP_NAME=""
TEST_NAME=""
QT_ENABLE="N"
VCPKG_PATH="~/Documents/cppEnv/DCEnv"
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
        -v|--vcpkg_path)
            VCPKG_PATH="$2"
            shift # past argument
            shift # past value
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
    PrepareMainProject ${MAIN_PROJECT_NAME} ${QT_ENABLE} ${VCPKG_PATH}
elif [[ ${EXTERNAL_PROJECT_NAME} != "" ]]; then
    PrepareExternalCMakeFile "Git" ${EXTERNAL_PROJECT_NAME} ./${EXTERNAL_PROJECT_NAME}.cmake
elif [[ ${LOCAL_PROJECT_NAME} != "" ]]; then
    PrepareExternalCMakeFile "Local" ${LOCAL_PROJECT_NAME} ./${LOCAL_PROJECT_NAME}.cmake
elif [[ ${STATIC_LIBRARY} != "" ]]; then
    PrepareLib "static" ${STATIC_LIBRARY} ${QT_ENABLE}
elif [[ ${DYNAMIC_LIBRARY} != "" ]]; then
    PrepareLib "dynamic" ${DYNAMIC_LIBRARY} ${QT_ENABLE}
elif [[ ${APP_NAME} != "" ]]; then
    PrepareApp ${APP_NAME} ${QT_ENABLE}
elif [[ ${TEST_NAME} != "" ]]; then
    PrepareTest ${TEST_NAME}
fi
