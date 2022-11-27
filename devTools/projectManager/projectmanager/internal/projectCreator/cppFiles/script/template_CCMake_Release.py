content_st = """
#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VCPKG_DIR="$SCRIPT_DIR/../vcpkg/scripts/buildsystems"
VCPKG_CMAKE="$VCPKG_DIR/vcpkg.cmake"

BUILD_TYPE="release"
INSTALL_DIR="../install"
SOURCE_DIR="../"
BUILD_FOLDER="../build_release"

if [ ! -d "$BUILD_FOLDER" ];
then
    mkdir $BUILD_FOLDER
fi

cd $BUILD_FOLDER

cmake -G Ninja ${SOURCE_DIR} -DCMAKE_BUILD_TYPE=${BUILD_TYPE} -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} -DCMAKE_TOOLCHAIN_FILE=${VCPKG_CMAKE}
"""
