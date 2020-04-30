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

mkdir -p $projectName/$projectName/src
mkdir -p $projectName/$projectName/lib/$projectName

# handle root CMakeLists.txt
cp ./$srcProject/CMakeLists.txt $projectName/$projectName
sed -i "s/$srcProject/$projectName/g" "$projectName/$projectName/CMakeLists.txt"
# handle lib CMakeLists.txt
cp ./$srcProject/lib/CMakeLists.txt $projectName/$projectName/lib
cp ./$srcProject/lib/$srcProject/CMakeLists.txt $projectName/$projectName/lib/$projectName
# handle src CMakeLists.txt
cp ./$srcProject/src/CMakeLists.txt $projectName/$projectName/src
sed -i "s/$srcProject/$projectName/g" "$projectName/$projectName/src/CMakeLists.txt"
