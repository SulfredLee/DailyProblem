content_st = """
git clone https://github.com/microsoft/vcpkg
cd ./vcpkg
./bootstrap-vcpkg.sh

./vcpkg search | grep gtest
./vcpkg install gtest
"""
