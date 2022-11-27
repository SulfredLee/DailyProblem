content_st = """

# This file is a template, and might need editing before it works on your project.
# This is a sample GitLab CI/CD configuration file that should run without any modifications.
# It demonstrates a basic 3 stage CI/CD pipeline. Instead of real tests or scripts,
# it uses echo commands to simulate the pipeline execution.
#
# A pipeline is composed of independent jobs that run scripts, grouped into stages.
# Stages run in sequential order, but jobs within stages run in parallel.
#
# For more information, see: https://docs.gitlab.com/ee/ci/yaml/index.html#stages
#
# You can copy and paste this template into a new `.gitlab-ci.yml` file.
# You should not add this template to an existing `.gitlab-ci.yml` file by using the `include:` keyword.
#
# To contribute improvements to CI/CD templates, please follow the Development guide at:
# https://docs.gitlab.com/ee/development/cicd/templates.html
# This specific template is located at:
# https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Getting-Started.gitlab-ci.yml

# https://docs.gitlab.com/ee/user/packages/generic_packages/index.html --- wget release package
# https://docs.gitlab.com/ee/ci/variables/predefined_variables.html --- predefined variables

stages:          # List of stages for jobs, and their order of execution
  - build-image
  - build-test
  - build-package
  - tag-release
  - deploy

variables:
  DOCKER_BUILDER_VERSION: builder_1.0.0
  DOCKER_RUNNER_VERSION: runner_1.0.0
  DOCKER_IMAGE_NAME_BUILDER: ${CI_REGISTRY_IMAGE}:${DOCKER_BUILDER_VERSION}
  CONTAINER_NAME_BUILDER: ${CI_PROJECT_NAME}_builder
  DOCKER_IMAGE_NAME_RUNNER: ${CI_REGISTRY_IMAGE}:${DOCKER_RUNNER_VERSION}
  CONTAINER_NAME_RUNNER: ${CI_PROJECT_NAME}_runner
  TEST_APP_NAME: ${CI_PROJECT_NAME}_Test
  RELEASE_NAME: ${CI_PROJECT_NAME}_Release
  PACKAGE_VERSION: "$CI_COMMIT_TAG"
  PACKAGE_REGISTRY_URL: "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/${RELEASE_NAME}/${PACKAGE_VERSION}"
  PACKAGE_NAME: "install_${PACKAGE_VERSION}.tar.gz"
  PACKAGE_VERSION_UAT: "$CI_COMMIT_REF_NAME"
  PACKAGE_REGISTRY_URL_UAT: "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/${RELEASE_NAME}/${PACKAGE_VERSION_UAT}"
  PACKAGE_NAME_UAT: "install_${PACKAGE_VERSION_UAT}.tar.gz"
  PYTHON_RELEASE_PATH: ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi

build-dev-image:
  stage: build-image
  image: docker:latest
  services:
    - docker:20.10.12-dind
  script:
    - docker login -u "gitlab-ci-token" -p $CI_JOB_TOKEN $CI_REGISTRY
    - docker build --target builder -t $DOCKER_IMAGE_NAME_BUILDER .
    - docker push $DOCKER_IMAGE_NAME_BUILDER
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      changes:
        - Dockerfile
    - when: never

build-run-image:
  stage: build-image
  image: docker:latest
  services:
    - docker:20.10.12-dind
  script:
    - docker login -u "gitlab-ci-token" -p $CI_JOB_TOKEN $CI_REGISTRY
    - docker build --target runner -t $DOCKER_IMAGE_NAME_RUNNER .
    - docker push $DOCKER_IMAGE_NAME_RUNNER
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      changes:
        - Dockerfile
    - when: never

build-test-app:       # This job runs in the build stage, which runs first.
  stage: build-test
  image: $DOCKER_IMAGE_NAME_BUILDER
  script:
    - /root/.local/bin/poetry install # duplicate prepare package
    - /root/.local/bin/poetry run python -m unittest discover tests # test application
  needs: []
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
    - when: never

uat-build-package-app:
  stage: build-package
  image: $DOCKER_IMAGE_NAME_BUILDER
  script:
    - tar -zcvf $PACKAGE_NAME_UAT ./*
    - |
      curl --header "JOB-TOKEN: ${CI_JOB_TOKEN}" --upload-file ./$PACKAGE_NAME_UAT ${PACKAGE_REGISTRY_URL_UAT}/$PACKAGE_NAME_UAT
  needs: []
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
    - when: never

prod-build-package-app:
  stage: build-package
  image: $DOCKER_IMAGE_NAME_BUILDER
  script:
    - tar -zcvf $PACKAGE_NAME ./*
    - |
      curl --header "JOB-TOKEN: ${CI_JOB_TOKEN}" --upload-file ./$PACKAGE_NAME ${PACKAGE_REGISTRY_URL}/$PACKAGE_NAME
  needs: []
  rules:
    - if: $CI_COMMIT_TAG
      when: always
    - when: never

release-app:
  stage: tag-release
  image: python:3.8
  script:
    - pip install poetry twine
    - poetry version ${CI_COMMIT_TAG}
    - poetry build
    - export TWINE_PASSWORD=${CI_JOB_TOKEN}
    - export TWINE_USERNAME=gitlab-ci-token
    - python -m twine upload --verbose --repository-url $PYTHON_RELEASE_PATH dist/*
  needs: ["prod-build-package-app"]
  rules:
    - if: $CI_COMMIT_TAG
      when: always
    - when: never

pages:
  stage: deploy
  image: $DOCKER_IMAGE_NAME_BUILDER
  script:
    - export PROJECT_VERSION=${CI_COMMIT_TAG:-latest}
    - doxygen
    - mv doxygen_doc/html/ public/
  artifacts:
    paths:
      - public
    expire_in: 1 week
  rules:
    - if: $CI_COMMIT_TAG
      when: always
    - when: never

uat-deploy:
  stage: deploy
  script:
    - echo "deploy to uat from branch $CI_COMMIT_REF_NAME"
  needs: ["uat-build-package-app"]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
    - when: never

prod-deploy:
  stage: deploy
  script:
    - echo "deploy to prod from tag $CI_COMMIT_TAG"
  needs: ["prod-build-package-app"]
  rules:
    - if: $CI_COMMIT_TAG
      when: manual
    - when: never
"""
