content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_BUILDER_VERSION:" ../../.gitlab-ci.yml | cut -c 27-)
docker run -it -v "${PWD}/../../:/cpp/project:rw" --env-file ./.env -u $(id -u):$(id -g) pm_test_cpp:${DOCKER_VERSION} bash -c "ln -s /cpp/vcpkg /cpp/project/; bash"
"""
