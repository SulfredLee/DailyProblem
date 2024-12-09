#!/bin/bash
buildPath="$PWD"

userRoot="/home/userName"
fwRoot="${userRoot}/your_framework_libraries"

## run the follow commands to see where does cpp compiler read header files?
# `gcc -print-prog-name=cc1plus` -v
# `gcc -print-prog-name=cpp` -v
## then you can copy the file to the gtags root path, usually that is /home/user
# rsync -zarv  --prune-empty-dirs --include "*/"  --include="*.h" --include="*.cpp" --include="*.c" --include="*.hpp" --exclude="*" "from" "to"
cppRoot=""


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
find -L ${fwRoot}/ -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq > gtags.files
find -L ${buildPath}/ -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq >> gtags.files
gtags

echo "######### make cscope"
find -L ${fwRoot} -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq > cscope.files
find -L ${buildPath} -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | sort | uniq >> cscope.files
cscope -q -R -b -k -i cscope.files
