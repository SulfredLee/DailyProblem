function PrintHelp {
    echo "Usage:"
    echo "\$ $0 --action <convert|check_status|gpu_usage> --input_video <video>"
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
            INTPUT_VIDEO="$2"
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
    local OUTPUT_VIDEO="converted_" + ${INPUT_VIDEO}
    echo "ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i ${INPUT_VIDEO} -c:a copy -c:v hevc_nvenc ${OUTPUT_VIDEO}"
    # ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i ${INPUT_VIDEO} -c:a copy -c:v hevc_nvenc ${OUTPUT_VIDEO}
elif [ "$ACTION" = "check_status" ]; then
    ffprob ${INPUT_VIDEO}
elif [ "$ACTION" = "gpu_usage" ]; then
    nvidia-smi -l 2
else
    echo "Action : ${ACTION} not recognized"
    PrintHelp
fi

