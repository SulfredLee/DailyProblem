content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../.gitlab-ci.yml | cut -c 27-)
docker build --build-arg DOCKER_UNAME=$(whoami)\
             --build-arg DOCKER_GNAME=$(whoami)\
             --build-arg DOCKER_UID=$(id -u)\
             --build-arg DOCKER_GID=$(id -g) --target builder -t flask_example_001:${DOCKER_VERSION}_$(whoami) ..

echo "$ cd ./dev"
# echo "$ docker-compose run {{ project_name }} bash" # old way
echo "$ ./start_dev_container.sh"
echo "poetry --version"
"""
