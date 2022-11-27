content_st = """
FROM python:3.12-rc-bullseye AS runner

RUN apt-get update
RUN apt-get -y install vim curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# init python package manager
WORKDIR /python/project/
COPY . /python/project
RUN /root/.local/bin/poetry install

FROM runner AS builder
RUN apt-get -y install git zip doxygen graphviz

"""
