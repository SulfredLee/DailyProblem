# Table of Contents
1. [CCreate Cheat Sheet](#ccreate-cheat-sheet)

# CCreate Cheat Sheet
## A simple project
``` Bash
# Create the whole project
$ CCreate.sh --main_project <YourProjectName>

# Go into the sub project and create application
$ cd ./YourProjectName/Projects/YourProjectName/app
$ CCreate.sh --app_name <YourAppName>

# Build and run
$ cd ./YourProjectName/Debug
$ ./runBuild.sh
$ ninja
$ ../Install/bin/YourAppName

# Output
Hello World
```

## Add static library
```Bash
# After you created a simple project
$ cd ./YourProjectName/Projects/YourProjectName/lib
$ CCreate.sh --static_library <YourLibName>

# Update CMakeLists.txt and build the library
$ cd ./YourProjectName/Projects/YourProjectName/
$ gvim CMakeLists.txt # update and build the lib subfolder

# Build and run (Same as before)
```

## Add dynamic library
```Bash
# After you created a simple project
$ cd ./YourProjectName/Projects/YourProjectName/lib
$ CCreate.sh --dynamic_library <YourLibName>

# Update CMakeLists.txt and build the library (Same as before)
# Build and run (Same as before)
```

## Add test sub project
```Bash
# After you created a simple project
$ cd ./YourProjectName/Projects/YourProjectName/test
$ CCreate.sh --test_name <TestName>

# Update CMakeLists.txt (Same as before)
# Build and run (Same as before)
```
