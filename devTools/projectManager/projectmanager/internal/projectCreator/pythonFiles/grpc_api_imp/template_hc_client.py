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
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_hc_logger", is_json_output=False)

    # get env variables
    env_v = {"host_name": os.getenv("GRPC_RUN_HOST", default="0.0.0.0")
             , "port": os.getenv("GRPC_RUN_PORT", default="50051")}
    logger.info(f"We get environment variables: {env_v}")

    try:
        with grpc.insecure_channel(f'{env_v["host_name"]}:{env_v["port"]}') as channel:
            stub = {{ project_name }}_pb2_grpc.{{ project_name_capitalize }}Stub(channel)

            pong = stub.HealthCheck({{ project_name }}_pb2.Ping(message="{{ project_name }} hc client"), timeout=5) # timeout in 5 second
            logger.info(f"Healthcheck response: {pong}")
    except Exception as e:
        logger.error("GRPC server is not healthy")
        logger.error(traceback.format_exc())
        exit(1)

if __name__ == "__main__":
    run()
"""
