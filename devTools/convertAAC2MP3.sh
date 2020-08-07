#/bin/sh
inputFile=$1
outputFile=${inputFile/aac/mp3}

ffmpeg -i ${inputFile} -c:a libmp3lame -ac 2 -q:a 2 ${outputFile}
