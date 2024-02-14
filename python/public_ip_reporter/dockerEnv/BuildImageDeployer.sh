
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_DEPLOYER_VERSION:" ../.gitlab-ci.yml | cut -c 28-)
docker build --file Dockerfile.Deploy             --target deployer -t public_ip_reporter:${DOCKER_VERSION}_$(whoami) ..

echo "$ Docker run -it public_ip_reporter:${DOCKER_VERSION}_${whoami}"