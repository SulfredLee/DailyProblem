content_st = """
from concurrent import futures
import time
import os
import grpc

import sfdevtools.observability.log_helper as lh

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm
import greet_pb2
import greet_pb2_grpc

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logger = mm.instance().get_logger()

        logger.info("SayHello Request Made:")
        logger.info(request)
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"

        return hello_reply

    def HealthCheck(self, request, context):
        logger = mm.instance().get_logger()

        logger.info(f"Healthcheck Request Made: {request.message}")
        pong = greet_pb2.Pong()
        pong.message = f"Pong from grpc server"

        return pong

    def ParrotSaysHello(self, request, context):
        logger = mm.instance().get_logger()

        logger.info("ParrotSaysHello Request Made:")
        logger.info(request)

        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i + 1}"
            yield hello_reply
            time.sleep(3)

    def ChattyClientSaysHello(self, request_iterator, context):
        logger = mm.instance().get_logger()

        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            logger.info("ChattyClientSaysHello Request Made:")
            logger.info(request)
            delayed_reply.request.append(request)

        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    def InteractingHello(self, request_iterator, context):
        logger = mm.instance().get_logger()

        for request in request_iterator:
            logger.info("InteractingHello Request Made:")
            logger.info(request)

            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name}"

            yield hello_reply

def serve():
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_server_logger", is_json_output=False)

    # get env variables
    env_v = {"host_name": os.getenv("GRPC_RUN_HOST", default="0.0.0.0")
             , "port": os.getenv("GRPC_RUN_PORT", default="50051")
             , "bucket_name": os.getenv("GRPC_BUCKET_NAME", default="dc-databucket")}
    logger.info(f"We get environment variables: {env_v}")

    main_m = mm.instance()
    main_m.init_component(logger=logger)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port(f'{env_v["host_name"]}:{env_v["port"]}')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
"""
