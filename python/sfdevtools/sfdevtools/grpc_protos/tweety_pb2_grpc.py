# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sfdevtools.grpc_protos.tweety_pb2 as tweety__pb2


class TweetyStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetStrategyConfigId = channel.unary_unary(
                '/tweety.Tweety/GetStrategyConfigId',
                request_serializer=tweety__pb2.GetStrategyConfigId_Msg.SerializeToString,
                response_deserializer=tweety__pb2.GetStrategyConfigId_Reply.FromString,
                )
        self.SaveStrategyConfig = channel.unary_unary(
                '/tweety.Tweety/SaveStrategyConfig',
                request_serializer=tweety__pb2.SaveStrategyConfig_Msg.SerializeToString,
                response_deserializer=tweety__pb2.SaveStrategyConfig_Reply.FromString,
                )
        self.HealthCheck = channel.unary_unary(
                '/tweety.Tweety/HealthCheck',
                request_serializer=tweety__pb2.Ping.SerializeToString,
                response_deserializer=tweety__pb2.Pong.FromString,
                )


class TweetyServicer(object):
    """The greeting service definition.
    """

    def GetStrategyConfigId(self, request, context):
        """Unary - request and respond
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveStrategyConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TweetyServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetStrategyConfigId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStrategyConfigId,
                    request_deserializer=tweety__pb2.GetStrategyConfigId_Msg.FromString,
                    response_serializer=tweety__pb2.GetStrategyConfigId_Reply.SerializeToString,
            ),
            'SaveStrategyConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveStrategyConfig,
                    request_deserializer=tweety__pb2.SaveStrategyConfig_Msg.FromString,
                    response_serializer=tweety__pb2.SaveStrategyConfig_Reply.SerializeToString,
            ),
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=tweety__pb2.Ping.FromString,
                    response_serializer=tweety__pb2.Pong.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tweety.Tweety', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Tweety(object):
    """The greeting service definition.
    """

    @staticmethod
    def GetStrategyConfigId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tweety.Tweety/GetStrategyConfigId',
            tweety__pb2.GetStrategyConfigId_Msg.SerializeToString,
            tweety__pb2.GetStrategyConfigId_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveStrategyConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tweety.Tweety/SaveStrategyConfig',
            tweety__pb2.SaveStrategyConfig_Msg.SerializeToString,
            tweety__pb2.SaveStrategyConfig_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tweety.Tweety/HealthCheck',
            tweety__pb2.Ping.SerializeToString,
            tweety__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)