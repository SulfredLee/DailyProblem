
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_RUNNER_VERSION:" ../.gitlab-ci.yml | cut -c 26-)
docker build --target runner -t microblog:${DOCKER_VERSION} ..