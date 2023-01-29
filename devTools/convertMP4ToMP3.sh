#!/bin/bash

initialPath=`pwd`
donePath="${initialPath}/done_folder"
totalWorkers=4

mkdir -p "${donePath}"

# ======================================== Function
function convertTask(){
    local inputFile=$1
    local donePath=$2
    local outputFile="${inputFile}.mp3"

    ffmpeg -i "$inputFile" "$outputFile"

    # prepare to remove original files
    mv "$inputFile" "${donePath}"
}
# ======================================== Main
for src_type in "*.mp4" "*.mpga"; do
    echo "Conversion start: ${src_type}"

    readarray -d '' movie_list < <(find "$initialPath" -type f -name "${src_type}" -print0)
    N=$totalWorkers
    curCount=0
    (
    for i in "${!movie_list[@]}"; do
        ((curCount=curCount%N)); ((curCount++==0)) && wait
        echo "conversion progress: $(( i + 1 ))/${#movie_list[@]}"

        convertTask "${movie_list[$i]}" "${donePath}" &
    done
    )

    echo "Conversion end: ${src_type}"
done

