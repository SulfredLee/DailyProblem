content_st = """
FROM python:3.12-rc-bullseye AS runner

ARG DOCKER_GID
ARG DOCKER_UID
ARG DOCKER_GNAME
ARG DOCKER_UNAME

RUN apt-get update
RUN apt-get -y install vim curl

# Create a group and user
RUN [ $DOCKER_UNAME = "root" ] && echo "No need to create root again" || ( groupadd -g $DOCKER_GID $DOCKER_GNAME && useradd -rm -d /home/$DOCKER_UNAME -s /bin/bash -g $DOCKER_GNAME -G sudo -u $DOCKER_UID $DOCKER_UNAME)
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

FROM runner AS builder
# need to redefine for different layers
ARG DOCKER_GID
ARG DOCKER_UID
ARG DOCKER_GNAME
ARG DOCKER_UNAME

# prepare python env for development
RUN mkdir -p /home/$DOCKER_UNAME/.cache/pypoetry/virtualenvs_mount

USER root
RUN apt-get -y install git zip doxygen graphviz
"""
