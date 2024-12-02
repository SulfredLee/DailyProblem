#!/bin/bash
buildPath="$PWD"

userRoot="/home/userName"
fwRoot="${userRoot}/your_framework_libraries"

cd ${userRoot}

# remove old tags
rm ${userRoot}/GPATH
rm ${userRoot}/GRTAGS
rm ${userRoot}/GTAGS
rm ${userRoot}/gtags.files



rm ${userRoot}/cscope.files
rm ${userRoot}/cscope.out
rm ${userRoot}/cscope.in.out
rm ${userRoot}/cscope.po.out



# make tags
echo "######### make GTag"
find -L ${fwRoot}/ ${buildPath} -type f -print > gtags.files
gtags

echo "######### make cscope"
find -L ${fwRoot} -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" > cscope.files
find -L ${buildPath} -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" >> cscope.files
cscope -q -R -b -k -i cscope.files
