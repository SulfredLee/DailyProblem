content_st = """
from concurrent import futures
import time
import os

import grpc
import sfdevtools.grpc_protos.{{ project_name }}_pb2 as {{ project_name }}_pb2
import sfdevtools.grpc_protos.{{ project_name }}_pb2_grpc as {{ project_name }}_pb2_grpc

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

import sfdevtools.observability.log_helper as lh

class {{ project_name_capitalize }}Servicer({{ project_name }}_pb2_grpc.{{ project_name_capitalize }}Servicer):
    def HealthCheck(self, request, context):
        logger = mm.instance().get_logger()

        logger.info(f"Healthcheck Request Made: {request.message}")
        pong = {{ project_name }}_pb2.Pong()
        pong.message = f"Pong from grpc server"

        return pong

def serve():
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_grpc_server_logger", is_json_output=False)

    # get env variables
    env_v = {"host_name": os.getenv("GRPC_RUN_HOST", default="0.0.0.0")
             , "port": os.getenv("GRPC_RUN_PORT", default="50051")
             , "bucket_name": os.getenv("GRPC_BUCKET_NAME", default="dc-databucket")}
    logger.info(f"We get environment variables: {env_v}")

    main_m = mm.instance()
    main_m.init_component(logger=logger)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    {{ project_name }}_pb2_grpc.add_{{ project_name_capitalize }}Servicer_to_server({{ project_name_capitalize }}Servicer(), server)
    server.add_insecure_port(f'{env_v["host_name"]}:{env_v["port"]}')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
"""
