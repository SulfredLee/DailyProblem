content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../../.gitlab-ci.yml | cut -c 27-)
rm -rf ${PWD}/../../virtualenvs/ || true
mkdir -p ${PWD}/../../virtualenvs/

# check if container exist
docker container list -a | grep {{ project_name }}:${DOCKER_VERSION}_$(whoami)
if [[ $? == 0 ]]; then
    # found exist container
    CONTAINER_ID=$(docker container list -a | grep {{ project_name }}:${DOCKER_VERSION}_$(whoami) | cut -d ' ' -f 1)

    # check if container already exited
    docker container list -a | grep {{ project_name }}:${DOCKER_VERSION}_$(whoami) | grep Exited
    if [[ $? == 0 ]]; then
        # found exited container
        docker start $CONTAINER_ID
    fi
    docker exec -it $CONTAINER_ID bash
else
    docker run -it -v "${PWD}/../../:/python/project:rw"\
                   -v "${PWD}/../../virtualenvs/:/home/$(whoami)/.cache/pypoetry/virtualenvs_mount/"\
                   --env-file ./.env -u $(id -u):$(id -g) {{ project_name }}:${DOCKER_VERSION}_$(whoami) bash -c "cp -rfL /home/$(whoami)/.cache/pypoetry/virtualenvs/* /home/$(whoami)/.cache/pypoetry/virtualenvs_mount/; bash"
fi
"""
