content_st = """
#!/bin/bash

DOCKER_VERSION=$(grep "DOCKER_RUNNER_VERSION:" ../.gitlab-ci.yml | cut -c 26-)
docker build --target runner -t pm_test_cpp:${DOCKER_VERSION} ..
"""
