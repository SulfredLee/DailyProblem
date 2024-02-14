
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_RUNNER_VERSION:" ../.gitlab-ci.yml | cut -c 26-)
docker build --file Dockerfile.Run             --build-arg DOCKER_UNAME=$(whoami)             --build-arg DOCKER_GNAME=$(id -g -n `whoami`)             --build-arg DOCKER_UID=$(id -u)             --build-arg DOCKER_GID=$(id -g) --target runner -t public_ip_reporter:${DOCKER_VERSION}_$(whoami) ..