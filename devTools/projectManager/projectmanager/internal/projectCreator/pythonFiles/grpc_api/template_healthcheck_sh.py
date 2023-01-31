content_st = """
#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR"

poetry run python hc_client.py

if [ $? -ge 1 ]; then
    echo "GRPC server is not healthy"
    exit 1
else
    echo "GRPC server is healthy"
    exit 0
fi
"""
