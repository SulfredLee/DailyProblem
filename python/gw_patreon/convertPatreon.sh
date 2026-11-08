#!/bin/bash

# initial
py_script_path="/home/sulfred/Documents/SoftwareDev/github/SulfredLee/DailyProblem/python/gw_patreon"
audio_path="/home/sulfred/Downloads/UMD4"
dry_run="True"

function PrintHelp {
    echo "Usage:"
    echo "\$ $0 --real-run --audio_path <your path> --py_script_path <python script path>"
}

# handle input arguments
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -h|--help)
            PrintHelp
            shift # past argument
            ;;
        -a|--audio_path)
            audio_path="$2"
            shift # past argument
            shift # past value
            ;;
        -p|--py_script_path)
            py_script_path="$2"
            shift # past argument
            shift # past value
            ;;
        -r|--real_run)
            dry_run="False"
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


# prepare python env
source ~/Documents/bin/start_conda.sh
conda activate py310_gw_patreon

if [ "$dry_run" = "True" ]; then
    python ${py_script_path}/convert_doc.py --dry-run ${audio_path}
    python ${py_script_path}/convert_sf.py --dry-run ${audio_path}
    python ${py_script_path}/convert_night.py --dry-run ${audio_path}
else
    python ${py_script_path}/convert_doc.py ${audio_path}
    python ${py_script_path}/convert_sf.py ${audio_path}
    python ${py_script_path}/convert_night.py ${audio_path}

fi
