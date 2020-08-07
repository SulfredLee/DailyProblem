#!/bin/bash
basePath=`pwd`
tempTagPath="$basePath/../tempTagFolder"
appFolders=("DatabaseMaintainer") # filter out

# move all folders beyond root
if [ ! -d "$tempTagPath" ]; then
    mkdir "$tempTagPath"
fi
if [ ! -d "$tempTagPath/app" ]; then
    mkdir "$tempTagPath/app"
fi
for folder in ${appFolders[@]}; do
    nextFolder="$basePath/app/$folder"
    mv $nextFolder $tempTagPath/app
done

prepareSpacemacsTags.sh

mv $tempTagPath/app/* ./app

if [ -d "$tempTagPath/app" ] && [ -z "$(ls -A $tempTagPath/app/)" ]; then
    rm -rf $tempTagPath/app
else
    echo "No need to have further action $tempTagPath/app"
fi
if [ -d "$tempTagPath" ] && [ -z "$(ls -A $tempTagPath)" ]; then
    rm -rf $tempTagPath
else
    echo "No need to have further action $tempTagPath"
fi
