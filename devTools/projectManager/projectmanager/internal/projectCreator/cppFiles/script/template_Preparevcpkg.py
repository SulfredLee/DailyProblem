content_st = """
# https://github.com/microsoft/vcpkg/blob/master/docs/examples/versioning.getting-started.md
cd ../{{ project_name }}
git clone https://github.com/microsoft/vcpkg
cd ./vcpkg
./bootstrap-vcpkg.sh

./vcpkg search | grep gtest
./vcpkg install gtest
"""
