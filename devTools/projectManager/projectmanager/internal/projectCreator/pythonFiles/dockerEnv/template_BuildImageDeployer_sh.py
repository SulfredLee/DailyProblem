content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_DEPLOYER_VERSION:" ../.gitlab-ci.yml | cut -c 28-)
docker build --file Dockerfile.Deploy\
             --target dev -t {{ project_name }}:${DOCKER_VERSION}_$(whoami) ..

echo "$ Docker run -it {{ project_name }}:${DOCKER_VERSION}_${whoami}"
"""
