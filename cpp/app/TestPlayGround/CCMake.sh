
function PrepareRunBuildFile {
    local buildType=$1
    local outputFile=$2

    echo "#!/bin/bash
    # example folder: /home/<user>/Documents/cppEnv/DCEnv/vcpkg/scripts/buildsystems/vcpkg.cmake
    toolChainFolder=\$1
    if [[ -z \${toolChainFolder} ]]; then
        cmake -G Ninja ../ -DCMAKE_BUILD_TYPE=${buildType} -DCMAKE_INSTALL_PREFIX=../install
    else
        cmake -G Ninja ../ -DCMAKE_BUILD_TYPE=${buildType} -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_TOOLCHAIN_FILE=\${toolChainFolder}/vcpkg/scripts/buildsystems/vcpkg.cmake
    fi
    " > ${outputFile}

    chmod +x ${outputFile}
}

function PrepareDebugBuild {
    local folderPath="debug"

    echo "Prepare Debug Folder"

    mkdir ${folderPath}
    mkdir -p install
    PrepareRunBuildFile "Debug" ${folderPath}/"CCMake.sh"
}

function PrepareReleaseBuild {
    local folderPath="release"

    echo "Prepare Release Folder"

    mkdir ${folderPath}
    mkdir -p install
    PrepareRunBuildFile "release" ${folderPath}/"CCMake.sh"
}

POSITIONAL=()
BUILD_TYPE=""
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -t|--build_type)
            BUILD_TYPE="$2"
            shift # past argument
            shift # past value
            ;;
        --default)
            DEFAULT=YES
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ ${BUILD_TYPE} == "debug" ]]; then
    PrepareDebugBuild
elif [[ ${BUILD_TYPE} == "release" ]]; then
    PrepareReleaseBuild
elif [[ ${BUILD_TYPE} == "" ]]; then
    PrepareDebugBuild
    PrepareReleaseBuild
fi

