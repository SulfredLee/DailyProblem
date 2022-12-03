content_st = """
FROM python:3.12-rc-bullseye AS runner

ARG DOCKER_GID
ARG DOCKER_UID

RUN apt-get update
RUN apt-get -y install vim curl

# Create a group and user
RUN [ $DOCKER_UID = "root" ] && echo "No need to create root again" || ( groupadd $DOCKER_GID && useradd $DOCKER_UID -m -g $DOCKER_GID)
# Tell docker that all future commands should run as the appuser user
USER $DOCKER_UID

RUN curl -sSL https://install.python-poetry.org | python3 -
# It is safe to add 2 paths, only one user is being using
ENV PATH="/home/$DOCKER_UID/.local/bin:$PATH"
ENV PATH="/root/.local/bin:$PATH"

# init python package manager
WORKDIR /python/project/
COPY . /python/project
RUN poetry install

FROM runner AS builder
# need to redefine for different layers
ARG DOCKER_GID
ARG DOCKER_UID

# prepare python env for development
RUN mkdir -p /home/$DOCKER_UID/.cache/pypoetry/virtualenvs_mount

USER root
RUN apt-get -y install git zip doxygen graphviz
"""
