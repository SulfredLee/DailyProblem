#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# config
rootActions=("Create Project" "Update Project")
createLanguageTypes=("Python" "Cpp")
updateLanguageTypes=("Cpp")

## create project selection
pythonProjectType=("Python Web Project" "Python General Project")
cppProjectType=("Cpp Project" "Cpp Static Lib Project" "Cpp Dynamic Lib Project" "Cpp QT Project" "Cpp QT Static Lib Project" "Cpp QT Dynamic Lib Project")
## udpate project selection
cppProjectUpdateType=("Add Thrid Party Project" "Add Sub Folder")

# functions
selectionResult=""
function getUserSelection {
    local selectionTopic="$1"
    shift
    local selections=("$@")

    echo $selectionTopic

    while true ; do
        for i in ${!selections[@]}; do
            echo "${i}. ${selections[$i]}"
        done
        echo ">=${#selections[@]}. quit"

        read -p "User selection: " selectionIndex

        # User select exist
        if [[ ${selectionIndex} -ge ${#selections[@]} ]]
        then
            echo "Exit"
            exit 0
        fi
        # User select correctly
        if [[ 0 -le ${selectionIndex} ]] && [[ ${selectionIndex} -lt ${#selections[@]} ]]
        then
            selectionResult=${selections[${selectionIndex}]}
            break
        fi
    done
}

# Main
echo "============ Welcome to $0 ============"

getUserSelection "============ Action Select ============" "${rootActions[@]}"
actionSelection=${selectionResult}
echo ${actionSelection}


selectionTitle="============ Language Select ============"
if [[ ${actionSelection} == "Create Project" ]]; then
    getUserSelection "${selectionTitle}" "${createLanguageTypes[@]}"
    languageSelection=${selectionResult}
    read -p "Project Name: " projectName
    echo "New project name: ${projectName}"
elif [[ ${actionSelection} == "Update Project" ]]; then
    getUserSelection "${selectionTitle}" "${updateLanguageTypes[@]}"
    languageSelection=${selectionResult}
else
    echo "Wrong actionSelection: ${actionSelection}"
    exit 0
fi

echo ${languageSelection}

selectionTitle="============ Project Select ============"
if [[ ${actionSelection} == "Create Project" ]]; then
    if [[ ${languageSelection} == "Python" ]]; then
        getUserSelection "${selectionTitle}" "${pythonProjectType[@]}"
        projectSelection=${selectionResult}
    elif [[ ${languageSelection} == "Cpp" ]]; then
        getUserSelection "${selectionTitle}" "${cppProjectType[@]}"
        projectSelection=${selectionResult}
    else
        echo "Wrong languageSelection: ${languageSelection}"
        exit 0
    fi
elif [[ ${actionSelection} == "Update Project" ]]; then
    if [[ ${languageSelection} == "Cpp" ]]; then
        getUserSelection "${selectionTitle}" "${cppProjectUpdateType[@]}"
        projectSelection=${selectionResult}
    else
        echo "Wrong languageSelection: ${languageSelection}"
        exit 0
    fi
fi


echo ""
echo ""
echo "Action: ${actionSelection}"
echo "Language: ${languageSelection}"
echo "Project: ${projectSelection}"

initial_path=`pwd`
echo "user call script from: ${initial_path}"

cd ${SCRIPT_DIR}
poetry update

# make python runable
export PYTHONPATH=${SCRIPT_DIR}
if [[ ${actionSelection} == "Create Project" ]]; then
    poetry run python ${SCRIPT_DIR}/projectmanager/app/main.py\
           --action "${actionSelection}"\
           --lang "${languageSelection}"\
           --projectType "${projectSelection}"\
           --projectName "${projectName}"\
           --projectPath "${initial_path}"
elif [[ ${actionSelection} == "Update Project" ]]; then
    poetry run python ${SCRIPT_DIR}/projectmanager/app/main.py --action "${actionSelection}" --lang "${languageSelection}" --projectType "${projectSelection}"
fi

cd -
