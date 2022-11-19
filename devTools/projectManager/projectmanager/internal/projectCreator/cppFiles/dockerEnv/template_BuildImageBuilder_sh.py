content_st = """
#!/bin/bash

docker build --target builder -t {{ project_name }}:builder_1.0.0 ..

echo "$ cd ./dev"
# echo "$ docker-compose run {{ project_name }} bash" # old way
echo "$ ./start_dev_container.sh"
"""
