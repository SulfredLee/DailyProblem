content_st = """
version: "3.3"
services:
  {{ project_name }}_run_env:
    image: "{{ project_name }}:runner_1.0.0"
    env_file:
      - ./.env
"""
