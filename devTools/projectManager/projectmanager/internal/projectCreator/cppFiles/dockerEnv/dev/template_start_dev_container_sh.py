content_st = """
#!/bin/bash

docker run -it -v "${PWD}/../../:/cpp/project:rw" -e TERM=xterm-256color -u $(id -u):$(id -g) {{ project_name }}:builder_1.0.0 bash -c "ln -s /cpp/vcpkg /cpp/project/; bash"
"""
