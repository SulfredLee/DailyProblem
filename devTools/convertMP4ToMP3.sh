#!/bin/bash

initialPath=`pwd`
donePath="${initialPath}/done_folder"

mkdir -p "${donePath}"

for src_type in "*.mp4" "*.mpga"; do
    echo "Conversion start: ${src_type}"

    readarray -d '' movie_list < <(find "$initialPath" -type f -name "${src_type}" -print0)
    for i in "${!movie_list[@]}"; do
        echo "conversion progress: $(( i + 1 ))/${#movie_list[@]}"
        ffmpeg -i "${movie_list[$i]}" "${movie_list[$i]}.mp3"

        # prepare to remove original files
        mv "${movie_list[$i]}" "${donePath}"
    done

    echo "Conversion end: ${src_type}"
done

