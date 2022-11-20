content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../.gitlab-ci.yml | cut -c 27-)
docker build --target builder -t {{ project_name }}:${DOCKER_VERSION} ..

echo "$ cd ./dev"
# echo "$ docker-compose run {{ project_name }} bash" # old way
echo "$ ./start_dev_container.sh"
echo "poetry location in container /root/.local/bin/poetry"
"""
