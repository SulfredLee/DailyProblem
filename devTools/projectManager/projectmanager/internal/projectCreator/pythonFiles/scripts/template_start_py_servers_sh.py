content_st = """
#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# start your server
cd "$SCRIPT_DIR"
cd ../{{ project_name }}/app/{{ app_subfolder }}/
poetry run flask run
# poetry run flask run &
cd -

# start your next server
"""
