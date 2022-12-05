content_st = """
# FROM ubuntu:16.04 AS runner
# FROM ubuntu:18.04 AS runner
# FROM ubuntu:20.04 AS runner
FROM ubuntu:22.04 AS runner

RUN apt-get update
RUN apt-get -y install vim

WORKDIR /cpp/project/

FROM runner AS builder
RUN apt-get -y install build-essential vim ninja-build cmake doxygen git gdb curl zip pkg-config doxygen graphviz

# init cpp package manager
WORKDIR /cpp/script/
COPY ./script/Preparevcpkg.sh /cpp/script/
RUN chmod +x Preparevcpkg.sh && ./Preparevcpkg.sh

WORKDIR /cpp/project/

# create user to avoid using root
ARG DOCKER_GID
ARG DOCKER_UID
ARG DOCKER_GNAME
ARG DOCKER_UNAME

# Create a group and user
RUN [ $DOCKER_UNAME = "root" ] && echo "No need to create root again" || ( groupadd -g $DOCKER_GID $DOCKER_GNAME || true && useradd -rm -d /home/$DOCKER_UNAME -s /bin/bash -g $DOCKER_GNAME -G sudo -u $DOCKER_UID $DOCKER_UNAME)

"""
