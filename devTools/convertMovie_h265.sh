#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
initialPath=`pwd`
echo "user call script from: ${initialPath}"

function PrintHelp {
    echo "Usage:"
    echo "\$ $0 --action <convert|check_status|gpu_usage|convert_recursive> --input_video <video>"
}

IS_LOW_QUALITY=0
function IsLowQuality {
    FILE_NAME=$1

    echo "IsLowQuality: $FILE_NAME"

    # get width
    MOVIE_WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=s=x:p=0 "$FILE_NAME")

    # get height
    MOVIE_HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=s=x:p=0 "$FILE_NAME")

    echo "Movie size: $MOVIE_WIDTH x $MOVIE_HEIGHT"

    if (( $MOVIE_WIDTH < 1280 )); then
        IS_LOW_QUALITY=1
    elif (( $MOVIE_HEIGHT < 1080 )); then
        IS_LOW_QUALITY=1
    else
        IS_LOW_QUALITY=0
    fi
}

POSITIONAL=()
ACTION=""
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
        -a|--action)
            ACTION="$2"
            shift # past argument
            shift # past value
            ;;
        -i|--input_video)
            INPUT_VIDEO="$2"
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



if [ "$ACTION" = "convert" ]; then
    OUTPUT_VIDEO="h265_${INPUT_VIDEO}"
    echo "ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i ${INPUT_VIDEO} -c:a copy -c:v hevc_nvenc ${OUTPUT_VIDEO}"
    # echo "ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i ${INPUT_VIDEO} -c:a copy -c:v h264_nvenc -b:v 5M ${OUTPUT_VIDEO}" # h264
    ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i ${INPUT_VIDEO} -c:a copy -c:v hevc_nvenc ${OUTPUT_VIDEO}
elif [ "$ACTION" = "check_status" ]; then
    ffprob ${INPUT_VIDEO}
elif [ "$ACTION" = "gpu_usage" ]; then
    nvidia-smi -l 2
elif [ "$ACTION" = "convert_recursive" ]; then
    readarray -d '' movie_list < <(find "$initialPath" -type f \( -name "*.mp4" -o -name "*.wmv" -o -name "*.mkv" \) -print0)
    ERROR_LOG_FILE="${initialPath}/convert_failed.log"
    for i in "${!movie_list[@]}"; do
        echo "conversion progress: $(( i + 1 ))/${#movie_list[@]}"
        IsLowQuality "${movie_list[$i]}"
        if [[ ${movie_list[$i]} == *"converted_"* || ${movie_list[$i]} == *"h265_"* ]]; then
           echo "conversion skip this is already converted: ${movie_list[$i]}"
        elif (( $IS_LOW_QUALITY == 1 )); then
           echo "Quality of the movie is too low, no need to convert"
        else
           INPUT_VIDEO="$(basename "${movie_list[$i]}")"
           VIDEO_PATH="$(dirname "${movie_list[$i]}")"
           OUTPUT_VIDEO="$VIDEO_PATH/h265_${INPUT_VIDEO}"
           if [[ ${INPUT_VIDEO} == *".wmv" ]]; then
              OUTPUT_VIDEO="$VIDEO_PATH/h265_${INPUT_VIDEO}.mp4"
           fi
           echo "conversion start: $VIDEO_PATH"
           echo ${movie_list[$i]}
           echo $INPUT_VIDEO
           echo $VIDEO_PATH
           echo $OUTPUT_VIDEO

           start_time=`date +%s`
           # ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i "${movie_list[$i]}" -c:a copy -c:v hevc_nvenc "${OUTPUT_VIDEO}"
	   ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "${movie_list[$i]}" -c:v hevc_nvenc "${OUTPUT_VIDEO}"
           if [[ $? -ne 0 ]]; then
               echo "Error found. Failed to convert ${movie_list[$i]}"
               echo "Error found. Failed to convert ${movie_list[$i]}" >> "${ERROR_LOG_FILE}"
           else
               end_time=`date +%s`
               run_time=$(( end_time - start_time ))

               run_time_human_readable=$(date -d@$run_time -u +%H:%M:%S) # convert second to Hour Minute Second
               echo "conversion done: $VIDEO_PATH, $run_time_human_readable"
               mv "${movie_list[$i]}" "${initialPath}"
           fi
        fi
    done
else
    echo "Action : ${ACTION} not recognized"
    PrintHelp
fi

