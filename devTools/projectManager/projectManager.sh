#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# config
rootActions=("Create Project" "Update Project")
createLanguageTypes=("Python" "Cpp" "Kubernetes")
updateLanguageTypes=("Cpp" "Python")

## create project selection
pythonProjectType=("Python Restful API Project" "Python General Project" "Python Web Site Project" "Python QC Project" "Python GRPC Project")
cppProjectType=("Cpp General Project")
k8sProjectType=("General Infra Project")
## udpate project selection
cppProjectUpdateType=("Add External Project" "Add Static Library" "Add Dynamic Library" "Add Simple App" "Add QT App" "Add QT Static Library" "Add QT Dynamic Library")
pythonProjectUpdateType=("Add GRPC Project" "Add Restful API Project" "Add Web Site Project")

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
    projectName="${projectName,,}"
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
    elif [[ ${languageSelection} == "Kubernetes" ]]; then
        getUserSelection "${selectionTitle}" "${k8sProjectType[@]}"
        projectSelection=${selectionResult}
    else
        echo "Wrong languageSelection: ${languageSelection}"
        exit 0
    fi
elif [[ ${actionSelection} == "Update Project" ]]; then
    if [[ ${languageSelection} == "Cpp" ]]; then
        getUserSelection "${selectionTitle}" "${cppProjectUpdateType[@]}"
        projectSelection=${selectionResult}
        read -p "Module Name: " moduleName
        echo "New module name: ${moduleName}"
    elif [[ ${languageSelection} == "Python" ]]; then
        getUserSelection "${selectionTitle}" "${pythonProjectUpdateType[@]}"
        projectSelection=${selectionResult}
        moduleName="No module name for python updates"
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

initialPath=`pwd`
echo "user call script from: ${initialPath}"

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
           --projectPath "${initialPath}"
elif [[ ${actionSelection} == "Update Project" ]]; then
    poetry run python ${SCRIPT_DIR}/projectmanager/app/main.py\
           --action "${actionSelection}"\
           --lang "${languageSelection}"\
           --projectType "${projectSelection}"\
           --projectPath "${initialPath}"\
           --moduleName "${moduleName}"
fi

cd -
