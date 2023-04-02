# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sfdevtools.grpc_protos.eagle_pb2 as eagle__pb2


class EagleStub(object):
    """The eagle service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
                '/eagle.Eagle/HealthCheck',
                request_serializer=eagle__pb2.Ping.SerializeToString,
                response_deserializer=eagle__pb2.Pong.FromString,
                )
        self.GetDataByStrategyId = channel.unary_unary(
                '/eagle.Eagle/GetDataByStrategyId',
                request_serializer=eagle__pb2.GetDataByStrategyId_Msg.SerializeToString,
                response_deserializer=eagle__pb2.GetDataByStrategyId_Reply.FromString,
                )
        self.GetBacktestWarmupData = channel.unary_unary(
                '/eagle.Eagle/GetBacktestWarmupData',
                request_serializer=eagle__pb2.GetBacktestWarmupData_Msg.SerializeToString,
                response_deserializer=eagle__pb2.GetBacktestWarmupData_Reply.FromString,
                )
        self.GetUSLEIData = channel.unary_unary(
                '/eagle.Eagle/GetUSLEIData',
                request_serializer=eagle__pb2.GetUSLEIData_Msg.SerializeToString,
                response_deserializer=eagle__pb2.GetUSLEIData_Reply.FromString,
                )


class EagleServicer(object):
    """The eagle service definition.
    """

    def HealthCheck(self, request, context):
        """Unary - request and respond
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataByStrategyId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBacktestWarmupData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUSLEIData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EagleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=eagle__pb2.Ping.FromString,
                    response_serializer=eagle__pb2.Pong.SerializeToString,
            ),
            'GetDataByStrategyId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataByStrategyId,
                    request_deserializer=eagle__pb2.GetDataByStrategyId_Msg.FromString,
                    response_serializer=eagle__pb2.GetDataByStrategyId_Reply.SerializeToString,
            ),
            'GetBacktestWarmupData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBacktestWarmupData,
                    request_deserializer=eagle__pb2.GetBacktestWarmupData_Msg.FromString,
                    response_serializer=eagle__pb2.GetBacktestWarmupData_Reply.SerializeToString,
            ),
            'GetUSLEIData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUSLEIData,
                    request_deserializer=eagle__pb2.GetUSLEIData_Msg.FromString,
                    response_serializer=eagle__pb2.GetUSLEIData_Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'eagle.Eagle', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Eagle(object):
    """The eagle service definition.
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
        return grpc.experimental.unary_unary(request, target, '/eagle.Eagle/HealthCheck',
            eagle__pb2.Ping.SerializeToString,
            eagle__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDataByStrategyId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eagle.Eagle/GetDataByStrategyId',
            eagle__pb2.GetDataByStrategyId_Msg.SerializeToString,
            eagle__pb2.GetDataByStrategyId_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBacktestWarmupData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eagle.Eagle/GetBacktestWarmupData',
            eagle__pb2.GetBacktestWarmupData_Msg.SerializeToString,
            eagle__pb2.GetBacktestWarmupData_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUSLEIData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eagle.Eagle/GetUSLEIData',
            eagle__pb2.GetUSLEIData_Msg.SerializeToString,
            eagle__pb2.GetUSLEIData_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
