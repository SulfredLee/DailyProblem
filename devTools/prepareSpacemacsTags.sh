#!/bin/bash
buildPath="$PWD"


# remove old tags
rm ${buildPath}/GPATH
rm ${buildPath}/GRTAGS
rm ${buildPath}/GTAGS

rm ${buildPath}/cscope.files
rm ${buildPath}/cscope.out
rm ${buildPath}/cscope.in.out
rm ${buildPath}/cscope.po.out

# make tags
echo "######### make GTag"
find -L ./ -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq > gtags.files
gtags

echo "######### make cscope"
find -L . -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq > cscope.files
cscope -q -R -b -k -i cscope.files
