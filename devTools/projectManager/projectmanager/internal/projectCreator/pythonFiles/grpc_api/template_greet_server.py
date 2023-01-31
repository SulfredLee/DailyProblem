content_st = """
from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logger = mm.instance().get_logger()

        logger.info("SayHello Request Made:")
        logger.info(request)
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"

        return hello_reply

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
    main_m = mm.instance()
    logger = main_m.get_logger()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
"""
