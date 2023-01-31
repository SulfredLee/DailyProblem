content_st = """
import greet_pb2_grpc
import greet_pb2
import time
import os
import grpc

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting = "Hello", name = name)
        yield hello_request
        time.sleep(1)

def run():
    logger = mm.instance().get_logger()

    # get env variables
    host_name = os.getenv("GRPC_RUN_HOST", default="localhost")
    port_num = os.getenv("GRPC_RUN_PORT", default="50051")
    logger.info(f"We get host name: {host_name} port number: {port_num}")

    with grpc.insecure_channel(f"{host_name}:{port_num}") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        logger.info("1. SayHello - Unary")
        logger.info("2. ParrotSaysHello - Server Side Streaming")
        logger.info("3. ChattyClientSaysHello - Client Side Streaming")
        logger.info("4. InteractingHello - Both Streaming")
        rpc_call = input("Which rpc would you like to make: ")

        if rpc_call == "1":
            hello_request = greet_pb2.HelloRequest(greeting = "Bonjour", name = "YouTube")
            hello_reply = stub.SayHello(hello_request)
            logger.info("SayHello Response Received:")
            logger.info(hello_reply)
        elif rpc_call == "2":
            hello_request = greet_pb2.HelloRequest(greeting = "Bonjour", name = "YouTube")
            hello_replies = stub.ParrotSaysHello(hello_request)

            for hello_reply in hello_replies:
                logger.info("ParrotSaysHello Response Received:")
                logger.info(hello_reply)
        elif rpc_call == "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())

            logger.info("ChattyClientSaysHello Response Received:")
            logger.info(delayed_reply)
        elif rpc_call == "4":
            responses = stub.InteractingHello(get_client_stream_requests())

            for response in responses:
                logger.info("InteractingHello Response Received: ")
                logger.info(response)

if __name__ == "__main__":
    run()
"""
