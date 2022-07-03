#!/bin/bash

# functions =============================================
safe_exit () {
    exit 0
}

ask_for_help () {
    this_script=`basename "$0"`
    echo "============================================="
    echo "How to use"
    echo "${this_script} --start_time HH:mm:ss --end_time HH:mm:ss --input_file xxx.mp4 [--dry_run]"
    echo "============================================="
    safe_exit
}

get_second_from_string () {
    TIMESTR=$1 # HH:mm:ss

    HH=${TIMESTR:0:2}
    mm=${TIMESTR:3:2}
    ss=${TIMESTR:6:2}

    total_second=$(( ${HH} * 3600 + ${mm} * 60 + ${ss} ))

    echo "${total_second}"
}

get_duration_string () {
    ENDTIME=$1 # second in integer
    STARTTIME=$2 # second in integer

    second_in_duration=$(( ENDTIME - STARTTIME ))

    HH=$(( ${second_in_duration} / 3600 ))
    second_in_duration=$(( ${second_in_duration} % 3600 ))
    mm=$(( ${second_in_duration} / 60 ))
    second_in_duration=$(( ${second_in_duration} % 60 ))
    ss=${second_in_duration}

    echo "${HH}:${mm}:${ss}"
}

# get parameters ========================================
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--start_time)
            STARTTIME="$2"
            shift # past argument
            shift # past value
            ;;
        -e|--end_time)
            ENDTIME="$2"
            shift # past argument
            shift # past value
            ;;
        -i|--input_file)
            INPUTFILE="$2"
            shift # past argument
            shift # past value
            ;;
        --help)
            ask_for_help
            shift # past argument
            ;;
        --dry_run)
            DRYRUN="True"
            shift # past argument
            ;;
        --default)
            DEFAULT=YES
            shift # past argument
            ;;
        -*|--*)
            echo "Unknown option $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1") # save positional arg
            shift # past argument
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# main ==================================================

# check inputs
if [ "$STARTTIME" == "" ]; then
    ask_for_help
elif [ "$ENDTIME" == "" ]; then
    ask_for_help
elif [ "$INPUTFILE" == "" ]; then
    ask_for_help
fi

# update imputs
CURTIME=$(date +"%Y%m%d_%H%M%S")
OUTPUTFILE="${CURTIME}_${INPUTFILE}"
STARTSEC=$(get_second_from_string ${STARTTIME})
ENDSEC=$(get_second_from_string ${ENDTIME})
DURATIONSTR=$(get_duration_string ${ENDSEC} ${STARTSEC})

# report inputs
echo "We will get movie slice from: ${INPUTFILE}"
echo "The start time is: ${STARTTIME}"
echo "The end time is: ${ENDTIME}"
echo "Output file: ${OUTPUTFILE}"

# run ffmpeg
echo ""
echo ""
echo "ffmpeg -ss ${STARTTIME} -t ${DURATIONSTR} -i ${INPUTFILE} -c copy ${OUTPUTFILE}"
if [ "$DRYRUN" != "True" ]; then
    ffmpeg -ss ${STARTTIME} -t ${DURATIONSTR} -i ${INPUTFILE} -c copy ${OUTPUTFILE}

    # new command supported by ffmpeg, with start and end time supported
    # ffmpeg -ss ${STARTTIME} -to ${ENDTIME} -i ${INPUTFILE} -c copy ${OUTPUTFILE}
fi
