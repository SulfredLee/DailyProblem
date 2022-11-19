content_st = """
# FROM ubuntu:16.04 AS runner
# FROM ubuntu:18.04 AS runner
# FROM ubuntu:20.04 AS runner
FROM ubuntu:22.04 AS runner

RUN apt-get update
RUN apt-get -y install vim

FROM runner AS builder
RUN apt-get -y install build-essential vim ninja-build cmake doxygen git gdb curl zip pkg-config

# init cpp package manager
WORKDIR /cpp/
COPY Preparevcpkg.sh /cpp/
RUN chmod +x Preparevcpkg.sh && ./Preparevcpkg.sh

WORKDIR /cpp/project/
"""
