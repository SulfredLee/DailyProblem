
#!/bin/bash

DOCKER_VERSION="1.0"
docker build --file Dockerfile.Dev             --build-arg DOCKER_UNAME=$(whoami)             --build-arg DOCKER_GNAME=$(id -g -n `whoami`)             --build-arg DOCKER_UID=$(id -u)             --build-arg DOCKER_GID=$(id -g) --target dev -t sulfredlee/sf_dev_ubuntu:${DOCKER_VERSION}_$(whoami) ..

echo "$ cd ./dev"
# echo "$ docker-compose run cpp_showcases bash" # old way
echo "$ ./start_dev_container.sh"
