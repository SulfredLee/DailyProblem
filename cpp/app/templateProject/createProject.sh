#!/bin/bash

# usage: ./createProject.sh ProjectName
#################################### Get Argument
projectName=""
if [ "$#" -eq 1 ]; then
    projectName=$1
else
    echo "usage ./createProject.sh ProjectName"
    exit
fi
srcProject="templateProject"

mkdir -p $projectName/Projects/$projectName
mkdir -p $projectName/Projects/$projectName/src
mkdir -p $projectName/Projects/$projectName/lib/$projectName
mkdir -p $projectName/debug
mkdir -p $projectName/release
mkdir -p $projectName/install

# handle root external cmake
cp $srcProject/Projects/CMakeLists.txt $projectName/Projects
sed -i "s/$srcProject/$projectName/g" "$projectName/Projects/CMakeLists.txt"
cp $srcProject/Projects/$srcProject.cmake $projectName/Projects/$projectName.cmake
sed -i "s/$srcProject/$projectName/g" "$projectName/Projects/$projectName.cmake"

# handle sub project
srcSubProjectRoot="$srcProject/Projects/$srcProject"
targetSubProjectRoot="$projectName/Projects/$projectName"
# handle root CMakeLists.txt
cp $srcSubProjectRoot/CMakeLists.txt $targetSubProjectRoot
sed -i "s/$srcProject/$projectName/g" "$targetSubProjectRoot/CMakeLists.txt"
# handle lib CMakeLists.txt
cp $srcSubProjectRoot/lib/CMakeLists.txt $targetSubProjectRoot/lib
cp $srcSubProjectRoot/lib/$srcProject/CMakeLists.txt $targetSubProjectRoot/lib/$projectName
# handle src CMakeLists.txt
cp $srcSubProjectRoot/src/CMakeLists.txt $targetSubProjectRoot/src
sed -i "s/$srcProject/$projectName/g" "$targetSubProjectRoot/src/CMakeLists.txt"

# copy ProjectB as an example
cp -rf $srcProject/Projects/ProjectB $projectName/Projects
cp $srcProject/Projects/ProjectB.cmake $projectName/Projects
