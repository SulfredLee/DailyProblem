SET script_path=%~dp0
echo %script_path:~0,-1%
SET buildPath=%cd%
echo %buildPath%

:: remove old tags
del ${buildPath}/GPATH
del ${buildPath}/GRTAGS
del ${buildPath}/GTAGS

del ${buildPath}/cscope.files
del ${buildPath}/cscope.out
del ${buildPath}/cscope.in.out
del ${buildPath}/cscope.po.out

:: make tags
echo "######### make GTag"
gtags.exe
echo "######### make cscope"
dir /b/s | findstr /i /r "\.c$ \.cpp$ \.cc$ \.h$ \.hpp$" > cscope.files
cscope.exe -q -R -b -k -i cscope.files
