
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_DEPLOYER_VERSION:" ../.gitlab-ci.yml | cut -c 28-)
docker build --file Dockerfile.Deploy             --target deployer -t german_learning_tools:${DOCKER_VERSION}_$(whoami) ..

echo "$ Docker run -it german_learning_tools:${DOCKER_VERSION}_${whoami}"