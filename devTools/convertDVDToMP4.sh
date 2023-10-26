#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
initialPath=`pwd`
echo "user call script from: ${initialPath}"

function PrintHelp {
    echo "Usage:"
    echo "\$ $0 --dvd_path <DVD path>"
}


POSITIONAL=()
DVD_PATH=""
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
        -d|--dvd_path)
            DVD_PATH="$2"
            shift # past argument
            shift # past value
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
    if [ -f "$DVD_PATH/VTS_01_7.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_7.VOB"
        cp "$DVD_PATH/VTS_01_7.VOB" "$DVD_PATH/VTS_01_6.VOB" "$DVD_PATH/VTS_01_5.VOB" "$DVD_PATH/VTS_01_4.VOB" "$DVD_PATH/VTS_01_3.VOB" "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_6.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_6.VOB"
        cp "$DVD_PATH/VTS_01_6.VOB" "$DVD_PATH/VTS_01_5.VOB" "$DVD_PATH/VTS_01_4.VOB" "$DVD_PATH/VTS_01_3.VOB" "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_5.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_5.VOB"
        cp "$DVD_PATH/VTS_01_5.VOB" "$DVD_PATH/VTS_01_4.VOB" "$DVD_PATH/VTS_01_3.VOB" "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_4.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_4.VOB"
        cp "$DVD_PATH/VTS_01_4.VOB" "$DVD_PATH/VTS_01_3.VOB" "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_3.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_3.VOB"
        cp "$DVD_PATH/VTS_01_3.VOB" "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_2.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_2.VOB"
        cp "$DVD_PATH/VTS_01_2.VOB" "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    elif [ -f "$DVD_PATH/VTS_01_1.VOB" ]; then
        echo "Found $DVD_PATH/VTS_01_1.VOB"
        cp "$DVD_PATH/VTS_01_1.VOB" "ConCat.vob"
    fi

    ffmpeg -loglevel warning -i "ConCat.vob" -codec:a copy -codec:v hevc_nvenc "converted.mp4"
else
    echo "Action : ${ACTION} not recognized"
    PrintHelp
fi
