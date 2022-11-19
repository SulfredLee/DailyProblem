content_st = """
# docker-compose run tt_build_env bash
# docker rm $(docker ps -a -f status=exited -q)

version: "3.3"
services:
  {{ project_name }}:
    image: "{{ project_name }}:builder_1.0.0"
    user: ${CUR_UID}:${CUR_GID}
    env_file:
      - ./.env
    volumes:
      - ../../:/cpp/project:rw
"""
