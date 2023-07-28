
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../.gitlab-ci.yml | cut -c 27-)
docker build --file Dockerfile.Dev             --build-arg DOCKER_UNAME=$(whoami)             --build-arg DOCKER_GNAME=$(id -g -n `whoami`)             --build-arg VSCODE_FLAG="no_vscode"             --build-arg DOCKER_UID=$(id -u)             --build-arg DOCKER_GID=$(id -g) --target dev -t german_learning_tools:${DOCKER_VERSION}_$(whoami) ..

echo "$ cd ./dev"
# echo "$ docker-compose run german_learning_tools bash" # old way
echo "$ ./start_dev_container.sh"
echo "poetry --version"
echo "For flask web app: poetry run flask run --host 0.0.0.0"