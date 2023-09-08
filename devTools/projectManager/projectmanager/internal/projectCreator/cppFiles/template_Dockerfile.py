content_st = """
# FROM ubuntu:16.04 AS builder
# FROM ubuntu:18.04 AS builder
FROM ubuntu:20.04 AS builder
# FROM ubuntu:22.04 AS builder
# FROM gcc:7.2.0 As builder

## for gcc specific version only --- install packages from repository
# learn from: https://unix.stackexchange.com/a/743843/56400
# there are 3 outdated sources in the file, we need to change it to the archive database so that we can install packages
#### $ cat /etc/apt/sources.list
#### deb http://deb.debian.org/debian stretch main
#### deb http://deb.debian.org/debian stretch-updates main
#### deb http://security.debian.org stretch/updates main

# RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
## for gcc specific version only --- end

RUN apt-get update
RUN apt-get -y install vim

WORKDIR /cpp/project/

FROM builder AS dev
# fix bug https://github.com/Netflix/security_monkey/issues/1197 --- hunged during Geographic area
ARG DEBIAN_FRONTEND=noninteractive

# autoconf used by libpqxx
RUN apt-get -y install build-essential vim ninja-build cmake doxygen git gdb curl zip pkg-config doxygen graphviz cscope global autoconf
RUN apt-get -y install qt5-default

# install cmake from script --- in case you need a newer cmake
# learn from: https://github.com/Rikorose/gcc-cmake/blob/master/Dockerfile
# ARG CMAKE_VERSION=3.16.3
# RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
#       -q -O /tmp/cmake-install.sh \
#       && chmod u+x /tmp/cmake-install.sh \
#       && mkdir /usr/bin/cmake \
#       && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
#       && rm /tmp/cmake-install.sh
# ENV PATH="/usr/bin/cmake/bin:${PATH}"

# init cpp package manager
WORKDIR /cpp/docker_scripts/
COPY ./scripts/Preparevcpkg.sh /cpp/docker_scripts/
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
