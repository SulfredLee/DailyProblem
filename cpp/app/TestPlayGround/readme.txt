# Usage:
cmake -G Ninja ../Projects -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../Install -DCMAKE_TOOLCHAIN_FILE=../Projects/vcpkg/scripts/buildsystems/vcpkg.cmake
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
export LD_LIBRARY_PATH=../Install/lib
