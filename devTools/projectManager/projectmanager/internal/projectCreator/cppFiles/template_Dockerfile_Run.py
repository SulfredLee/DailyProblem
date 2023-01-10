content_st = """
# FROM ubuntu:16.04 AS runner
# FROM ubuntu:18.04 AS runner
# FROM ubuntu:20.04 AS runner
FROM ubuntu:22.04 AS runner

RUN apt-get update
RUN apt-get -y install vim

WORKDIR /cpp/project/

# TODO: install the application

# TODO: your commands for application running
"""
