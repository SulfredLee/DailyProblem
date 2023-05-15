content_st = """
# FROM python:3.12-rc-bullseye AS builder
# FROM python:3.11.1-bullseye AS builder
# FROM python:3.10.9-bullseye AS builder
# FROM python:3.9.15-bullseye AS builder
FROM python:3.8.16-bullseye AS builder
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit --- prepare nvidia container before tensorflow
# https://www.tensorflow.org/install/docker --- tensorflow documentation
# FROM tensorflow/tensorflow:latest-gpu AS builder

ARG DOCKER_GID
ARG DOCKER_UID
ARG DOCKER_GNAME
ARG DOCKER_UNAME

RUN apt-get update
RUN apt-get -y install vim curl

# Create a group and user
RUN [ $DOCKER_UNAME = "root" ] && echo "No need to create root again" || ( groupadd -g $DOCKER_GID $DOCKER_GNAME || true && useradd -rm -d /home/$DOCKER_UNAME -s /bin/bash -g $DOCKER_GNAME -G sudo -u $DOCKER_UID $DOCKER_UNAME)
# Tell docker that all future commands should run as the appuser user
USER $DOCKER_UNAME

RUN curl -sSL https://install.python-poetry.org | python3 -
# It is safe to add 2 paths, only one user is being using
ENV PATH="/home/$DOCKER_UNAME/.local/bin:$PATH"
ENV PATH="/root/.local/bin:$PATH"

# init python package manager
WORKDIR /python/project/
COPY . /python/project
RUN poetry install

FROM builder AS dev
# need to redefine for different layers
ARG DOCKER_GID
ARG DOCKER_UID
ARG DOCKER_GNAME
ARG DOCKER_UNAME
ARG VSCODE_FLAG

USER root
# install package for documentation
RUN apt-get -y install git zip doxygen graphviz

# install vscode server
RUN [ $VSCODE_FLAG = "no_vscode" ] && echo "No need to install vscode server" || ( chmod +x scripts/install.vscode.sh && ./scripts/install.vscode.sh )
# install vscode package
USER $DOCKER_UNAME
RUN [ $VSCODE_FLAG = "no_vscode" ] && echo "No need to install vscode server" || code --install-extension ms-python.python ms-python.vscode-pylance
"""
