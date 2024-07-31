#/bin/sh
inputFile=$1
outputFile=convert.${inputFile}

opencc -i "$inputFile" -o "$outputFile" -c /usr/share/opencc/s2hk.json
