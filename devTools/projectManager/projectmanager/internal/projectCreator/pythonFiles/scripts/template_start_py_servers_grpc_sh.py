content_st = """
#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# start your server
cd "$SCRIPT_DIR"
cd ../{{ project_name }}/app/{{ app_subfolder }}/
poetry run python {{ project_name }}_grpc_server.py
# poetry run python {{ project_name }}_grpc_server.py &
cd -

# start your next server
"""
