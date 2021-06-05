# Table of Contents
1. [CCreate Cheat Sheet](#ccreate-cheat-sheet)

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
