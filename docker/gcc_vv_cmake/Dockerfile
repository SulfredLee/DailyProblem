ARG GCC_VERSION=7.2.0
FROM gcc:$GCC_VERSION As builder

# install packages from repository
# learn from: https://unix.stackexchange.com/a/743843/56400
# there are 3 outdated sources in the file, we need to change it to the archive database so that we can install packages
# $ cat /etc/apt/sources.list
#### deb http://deb.debian.org/debian stretch main
#### deb http://deb.debian.org/debian stretch-updates main
#### deb http://security.debian.org stretch/updates main
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install vim ninja-build cmake doxygen git gdb curl zip pkg-config doxygen graphviz cscope global autoconf

# install cmake from script
# learn from: https://github.com/Rikorose/gcc-cmake/blob/master/Dockerfile
# ARG CMAKE_VERSION=3.16.3
# RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
#       -q -O /tmp/cmake-install.sh \
#       && chmod u+x /tmp/cmake-install.sh \
#       && mkdir /usr/bin/cmake \
#       && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
#       && rm /tmp/cmake-install.sh
# ENV PATH="/usr/bin/cmake/bin:${PATH}"
