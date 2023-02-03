content_st = """
import sfdevtools.grpc_protos.{{ project_name }}_pb2 as {{ project_name }}_pb2
import sfdevtools.grpc_protos.{{ project_name }}_pb2_grpc as {{ project_name }}_pb2_grpc
import time
import os
import grpc
import traceback

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

import sfdevtools.observability.log_helper as lh

def run():
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_grpc_client_logger", is_json_output=False)

    # get env variables
    env_v = {"host_name": os.getenv("GRPC_RUN_HOST", default="0.0.0.0")
             , "port": os.getenv("GRPC_RUN_PORT", default="50051")
             , "bucket_name": os.getenv("GRPC_BUCKET_NAME", default="dc-databucket")}
    logger.info(f"We get environment variables: {env_v}")

    main_m = mm.instance()
    main_m.init_component(logger=logger)

    with grpc.insecure_channel(f'{env_v["host_name"]}:{env_v["port"]}') as channel:
        stub = {{ project_name }}_pb2_grpc.{{ project_name_capitalize }}Stub(channel)

if __name__ == "__main__":
    run()
"""
