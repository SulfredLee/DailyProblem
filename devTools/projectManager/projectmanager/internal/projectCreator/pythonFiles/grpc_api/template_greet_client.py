content_st = """
import greet_pb2_grpc
import greet_pb2
import time
import os
import grpc
import traceback

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

import sfdevtools.observability.log_helper as lh

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        try:
            hello_request = greet_pb2.HelloRequest(greeting = "Hello", name = name)
            yield hello_request
            time.sleep(1)
        except Exception:
            print(traceback.format_exc())

def run():
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_client_logger", is_json_output=False)

    # get env variables
    env_v = {"host_name": os.getenv("GRPC_RUN_HOST", default="0.0.0.0")
             , "port": os.getenv("GRPC_RUN_PORT", default="50051")
             , "bucket_name": os.getenv("GRPC_BUCKET_NAME", default="dc-databucket")}
    logger.info(f"We get environment variables: {env_v}")

    main_m = mm.instance()
    main_m.init_component(logger=logger)

    with grpc.insecure_channel(f'{env_v["host_name"]}:{env_v["port"]}') as channel:
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
