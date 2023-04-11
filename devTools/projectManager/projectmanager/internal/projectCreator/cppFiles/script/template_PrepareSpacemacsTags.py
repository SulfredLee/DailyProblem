content_st = """
#!/bin/bash
cd ../project/
# buildPath="$PWD"
buildPath="."


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
gtags
echo "######### make cscope"
find . -name "*.cc" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" > cscope.files
cscope -q -R -b -k -i cscope.files
"""
