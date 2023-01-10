content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_RUNNER_VERSION:" ../.gitlab-ci.yml | cut -c 26-)
docker build --file Dockerfile.Run --target runner -t {{ project_name }}:${DOCKER_VERSION} ..
"""
