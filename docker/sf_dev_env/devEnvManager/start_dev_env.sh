#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

DOCKER_VERSION="ubuntu_22_1.0"
DOCKER_NAME="sulfredlee/sf_dev_env"
DOCKER_WORKDIR="/SoftwareDev_Docker"
HOST_WORKDIR="${PWD}"

# check if container exist
docker container list -a | grep ${DOCKER_NAME}:${DOCKER_VERSION}
if [[ $? == 0 ]]; then
    # found exist container
    CONTAINER_ID=$(docker container list -a | grep ${DOCKER_NAME}:${DOCKER_VERSION} | cut -d ' ' -f 1)

    # check if container already exited
    docker container list -a | grep ${DOCKER_NAME}:${DOCKER_VERSION} | grep Exited
    if [[ $? == 0 ]]; then
        # found exited container
        docker start $CONTAINER_ID
    fi
    docker exec -it $CONTAINER_ID bash
else
    # using enviroment variable DISPLAY for running gui application within docker container https://stackoverflow.com/a/75336008/2358836
    docker run -it -v "${HOST_WORKDIR}/:${DOCKER_WORKDIR}:rw"\
            -v "/tmp/.X11-unix:/tmp/.X11-unix"\
            -v "/sys/fs/cgroup:/sys/fs/cgroup:ro"\
            -v "${HOME}/.ssh:/home/sulfred/.ssh:ro"\
            --env-file ${SCRIPT_DIR}/.env\
            -e DISPLAY=$DISPLAY\
            -u $(id -u):$(id -g)\
            ${DOCKER_NAME}:${DOCKER_VERSION} bash -c "bash"
fi
