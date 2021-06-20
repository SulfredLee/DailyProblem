# Table of Contents
- [CCreate Cheat Sheet](#ccreate-cheat-sheet)
- [vcpkg Cheat Sheet](#vcpkg-cheat-sheet)

# CCreate Cheat Sheet
``` Bash
Usage:
# Create main project
$ /home/sulfred/Documents/bin/CCreate.sh --main_project <YourProjectName>
$ /home/sulfred/Documents/bin/CCreate.sh --main_project <YourProjectName> --qt_enable
$ /home/sulfred/Documents/bin/CCreate.sh --main_project <YourProjectName> --vcpkg_path <ThePath>

# Create app
$ cd ./<YourProjectName>/app
$ /home/sulfred/Documents/bin/CCreate.sh --app_name <YourApp>
$ /home/sulfred/Documents/bin/CCreate.sh --app_name <YourApp> --qt_enable

# Create static library
$ cd ./<YourProjectName>/lib
$ /home/sulfred/Documents/bin/CCreate.sh --static_library <YourLibName>
$ /home/sulfred/Documents/bin/CCreate.sh --static_library <YourLibName> --qt_enable

# Create dynamic library
$ cd ./<YourProjectName>/lib
$ /home/sulfred/Documents/bin/CCreate.sh --dynamic_library <YourLibName>
$ /home/sulfred/Documents/bin/CCreate.sh --dynamic_library <YourLibName> --qt_enable

# Create test sub project
$ cd ./<YourProjectName/test
$ /home/sulfred/Documents/bin/CCreate.sh --test_name <TestName>
```

## QT Example
```Bash
$ /home/sulfred/Documents/bin/CCreate.sh --main_project <YourProjectName> --qt_enable

# Create app
$ cd ./<YourProjectName/app
$ /home/sulfred/Documents/bin/CCreate.sh --app_name <YourApp> --qt_enable

# Create lib
$ cd ./<YourProjectName>/lib
$ /home/sulfred/Documents/bin/CCreate.sh --static_library <YourLibName> --qt_enable
# Use QT creater to create a mainwindow class or dialog class to your lib folder
YourLibName/
├── CMakeLists.txt
├── mainwindow.cpp
├── mainwindow.h
└── mainwindow.ui
```

# VCPKG Cheat Sheet

```Bash
# Install vcpkg
git clone https://github.com/microsoft/vcpkg
./bootstrap-vcpkg.sh

# Manage package
./vcpkg list
./vcpkg search | grep json
./vcpkg install xxx
```
