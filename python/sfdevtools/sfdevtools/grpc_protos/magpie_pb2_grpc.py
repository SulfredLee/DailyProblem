# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sfdevtools.grpc_protos.magpie_pb2 as magpie__pb2


class MagpieStub(object):
    """The magpie service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
                '/magpie.Magpie/HealthCheck',
                request_serializer=magpie__pb2.Ping.SerializeToString,
                response_deserializer=magpie__pb2.Pong.FromString,
                )
        self.UpdateRefDataPriceFromQC = channel.unary_unary(
                '/magpie.Magpie/UpdateRefDataPriceFromQC',
                request_serializer=magpie__pb2.UpdateRefDataPriceFromQC_Msg.SerializeToString,
                response_deserializer=magpie__pb2.NoneReply.FromString,
                )
        self.UpdateRefDataFromQC = channel.unary_unary(
                '/magpie.Magpie/UpdateRefDataFromQC',
                request_serializer=magpie__pb2.UpdateRefDataFromQC_Msg.SerializeToString,
                response_deserializer=magpie__pb2.NoneReply.FromString,
                )


class MagpieServicer(object):
    """The magpie service definition.
    """

    def HealthCheck(self, request, context):
        """Unary - request and respond
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRefDataPriceFromQC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRefDataFromQC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MagpieServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=magpie__pb2.Ping.FromString,
                    response_serializer=magpie__pb2.Pong.SerializeToString,
            ),
            'UpdateRefDataPriceFromQC': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateRefDataPriceFromQC,
                    request_deserializer=magpie__pb2.UpdateRefDataPriceFromQC_Msg.FromString,
                    response_serializer=magpie__pb2.NoneReply.SerializeToString,
            ),
            'UpdateRefDataFromQC': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateRefDataFromQC,
                    request_deserializer=magpie__pb2.UpdateRefDataFromQC_Msg.FromString,
                    response_serializer=magpie__pb2.NoneReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'magpie.Magpie', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Magpie(object):
    """The magpie service definition.
    """

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
        return grpc.experimental.unary_unary(request, target, '/magpie.Magpie/HealthCheck',
            magpie__pb2.Ping.SerializeToString,
            magpie__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateRefDataPriceFromQC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/magpie.Magpie/UpdateRefDataPriceFromQC',
            magpie__pb2.UpdateRefDataPriceFromQC_Msg.SerializeToString,
            magpie__pb2.NoneReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateRefDataFromQC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/magpie.Magpie/UpdateRefDataFromQC',
            magpie__pb2.UpdateRefDataFromQC_Msg.SerializeToString,
            magpie__pb2.NoneReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
