content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../../.gitlab-ci.yml | cut -c 27-)
mkdir -p ${PWD}/../../virtualenvs/
docker run -it -v "${PWD}/../../:/python/project:rw"\
               -v "${PWD}/../../virtualenvs/:/home/$(whoami)/.cache/pypoetry/virtualenvs_mount/"\
               --env-file ./.env -u $(id -u):$(id -g) {{ project_name }}:${DOCKER_VERSION}_$(whoami) bash -c "cp -rf /home/$(whoami)/.cache/pypoetry/virtualenvs/* /home/$(whoami)/.cache/pypoetry/virtualenvs_mount/; bash"
"""
