#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
initialPath=`pwd`
echo "user call script from: ${initialPath}"

function PrintHelp {
    echo "Usage:"
    echo "\$ $0 (--dvd_path|-p) <DVD path> (--dry_run|-d)"
}


POSITIONAL=()
DVD_PATH=""
DRY_RUN=""
CURRENT_DATE=`date +%Y%m%d`
#can specify a date(YYYYMMDD) for which the script will re-generate (for T-1)

# handle input arguments
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -h|--help)
            PrintHelp
            shift # past argument
            ;;
        -p|--dvd_path)
            DVD_PATH="$2"
            shift # past argument
            shift # past value
            ;;
        -d|--dry_run)
            DRY_RUN="true"
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters



if [ "$DVD_PATH" != "" ]; then
    echo "copy VOB files from: $DVD_PATH"

    # get the list of files
    # sometime the VTS_01_01.VOB is the declaration of FBI warning, you may want to skip it manually
    readarray -d '' movie_list < <(find "$DVD_PATH" -type f \( -name "VTS_01_*.VOB" \) -print0)
    FILE_LIST=""
    for i in "${!movie_list[@]}"; do
        echo "Get file: ${movie_list[$i]}"
        FILE_LIST="${FILE_LIST} ${movie_list[$i]}"
    done
    CMD_LINE="cat ${FILE_LIST} > ConCat.vob"
    echo "${CMD_LINE}"
    if [ "$DRY_RUN" != "true" ]; then
        eval "$CMD_LINE"
    fi

    echo "ffmpeg -i \"ConCat.vob\" -c:a copy -c:s copy -c:v hevc_nvenc \"converted.mp4\""
    if [ "$DRY_RUN" != "true" ]; then
        ffmpeg -i "ConCat.vob" -c:a copy -c:v hevc_nvenc "converted.mp4"
        # you can use map to select the channel you want
        # https://trac.ffmpeg.org/wiki/Map
    fi
else
    echo "Action : ${ACTION} not recognized"
    PrintHelp
fi
