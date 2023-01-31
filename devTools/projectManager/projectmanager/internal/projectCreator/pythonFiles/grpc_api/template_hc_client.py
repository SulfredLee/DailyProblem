content_st = """
import greet_pb2_grpc
import greet_pb2
import time
import os
import grpc
import traceback

from peacock.app.grpc_api.main_manager import MainManager as mm

def run():
    logger = mm.instance().get_logger()

    # get env variables
    host_name = os.getenv("GRPC_RUN_HOST", default="localhost")
    port_num = os.getenv("GRPC_RUN_PORT", default="50051")
    logger.info(f"We get host name: {host_name} port number: {port_num}")

    try:
        with grpc.insecure_channel(f"{host_name}:{port_num}") as channel:
            stub = greet_pb2_grpc.GreeterStub(channel)

            pong = stub.HealthCheck(greet_pb2.Ping(message=""), timeout=5) # timeout in 5 second
            logger.info(f"Healthcheck response: {pong}")
    except Exception as e:
        logger.error("GRPC server is not healthy")
        logger.error(traceback.format_exc())
        exit(1)

if __name__ == "__main__":
    run()
"""
