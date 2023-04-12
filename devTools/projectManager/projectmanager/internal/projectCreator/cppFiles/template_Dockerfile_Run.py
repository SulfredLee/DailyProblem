content_st = """
# FROM ubuntu:16.04 AS runner
# FROM ubuntu:18.04 AS runner
FROM ubuntu:20.04 AS runner
# FROM ubuntu:22.04 AS runner

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install vim gdb curl zip qt5-default

WORKDIR /cpp/project/

# install the application
ARG PACKAGE_NAME
ARG CI_JOB_TOKEN
ARG PACKAGE_REGISTRY_URL

RUN curl -o $PACKAGE_NAME --header "JOB-TOKEN: ${CI_JOB_TOKEN}" ${PACKAGE_REGISTRY_URL}/$PACKAGE_NAME
RUN tar -xf $PACKAGE_NAME

# your commands for application running
CMD ["bash", "./scripts/Start_CPP_Servers.sh"]
"""
