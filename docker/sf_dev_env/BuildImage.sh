
#!/bin/bash

DOCKER_VERSION="ubuntu_24_6.0"
DOCKER_NAME="sulfredlee/sf_dev_env"
DOCKER_BUILD_PATH="."
DOCKER_FILE="Dockerfile.Ubuntu.24.6"
DOCKER_TARGET="round1"

# docker build --file ${DOCKER_FILE} \
#        --build-arg DOCKER_UNAME=$(whoami) \
#        --build-arg DOCKER_GNAME=$(id -g -n `whoami`) \
#        --build-arg DOCKER_UID=$(id -u) \
#        --build-arg DOCKER_GID=$(id -g) \
#        --target ${DOCKER_TARGET} \
#        -t ${DOCKER_NAME}:${DOCKER_VERSION} ${DOCKER_BUILD_PATH}
docker build --file ${DOCKER_FILE} \
       --build-arg DOCKER_UNAME=dev_user \
       --build-arg DOCKER_GNAME=dev_user \
       --build-arg DOCKER_UID=1000 \
       --build-arg DOCKER_GID=1000 \
       --target ${DOCKER_TARGET} \
       -t ${DOCKER_NAME}:${DOCKER_VERSION} ${DOCKER_BUILD_PATH}

# echo "$ docker-compose run cpp_showcases bash" # old way
echo "$ Install the devEnvManager then run the script start_dev_env.sh"
