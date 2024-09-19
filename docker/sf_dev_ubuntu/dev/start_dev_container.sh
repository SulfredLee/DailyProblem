
#!/bin/bash

DOCKER_VERSION="1.0"

# check if container exist
docker container list -a | grep sulfredlee/sf_dev_ubuntu:${DOCKER_VERSION}_$(whoami)
if [[ $? == 0 ]]; then
    # found exist container
    CONTAINER_ID=$(docker container list -a | grep sulfredlee/sf_dev_ubuntu:${DOCKER_VERSION}_$(whoami) | cut -d ' ' -f 1)

    # check if container already exited
    docker container list -a | grep sulfredlee/sf_dev_ubuntu:${DOCKER_VERSION}_$(whoami) | grep Exited
    if [[ $? == 0 ]]; then
        # found exited container
        docker start $CONTAINER_ID
    fi
    docker exec -it $CONTAINER_ID bash
else
    # using enviroment variable DISPLAY for running gui application within docker container https://stackoverflow.com/a/75336008/2358836
    docker run -it -v "${PWD}/../../:/SoftwareDev_Docker:rw"\
            -v "/tmp/.X11-unix:/tmp/.X11-unix"\
            -v "/sys/fs/cgroup:/sys/fs/cgroup:ro"\
            --env-file ./.env\
            -e DISPLAY=$DISPLAY\
            -u $(id -u):$(id -g)\
            sulfredlee/sf_dev_ubuntu:${DOCKER_VERSION}_$(whoami) bash -c "bash"
fi
