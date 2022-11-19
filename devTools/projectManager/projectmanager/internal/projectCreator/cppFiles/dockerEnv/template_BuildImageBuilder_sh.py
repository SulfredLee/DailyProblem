content_st = """
#!/bin/bash

docker build --target builder -t {{ project_name }}_build_env:1.0.0 .

echo "$ cd ./dev"
echo "$ docker-compose run {{ project_name }}_build_env bash"
"""
