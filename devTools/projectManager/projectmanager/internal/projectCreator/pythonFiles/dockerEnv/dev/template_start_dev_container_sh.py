content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../../.gitlab-ci.yml | cut -c 27-)
docker run -it -v "${PWD}/../../:/python/project:rw" --env-file ./.env {{ project_name }}:${DOCKER_VERSION} bash
"""
