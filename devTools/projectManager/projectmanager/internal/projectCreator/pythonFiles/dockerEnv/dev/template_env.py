content_st = """
# id -u
CUR_UID={{ cur_uid }}
# id -g
CUR_GID={{ cur_gid }}

FLASK_APP=app
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000

GRPC_RUN_HOST=localhost
GRPC_RUN_PORT=50051

TERM=xterm-256color
"""
