# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sfdevtools.grpc_protos.peacock_pb2 as peacock__pb2


class PeacockStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveFileToColud = channel.unary_unary(
                '/peacock.Peacock/SaveFileToColud',
                request_serializer=peacock__pb2.SaveFileToColud_Msg.SerializeToString,
                response_deserializer=peacock__pb2.NoneReply.FromString,
                )
        self.SaveRefDataPriceFromQC = channel.unary_unary(
                '/peacock.Peacock/SaveRefDataPriceFromQC',
                request_serializer=peacock__pb2.SaveRefDataPriceFromQC_Msg.SerializeToString,
                response_deserializer=peacock__pb2.NoneReply.FromString,
                )
        self.SaveRefDataFromQC = channel.unary_unary(
                '/peacock.Peacock/SaveRefDataFromQC',
                request_serializer=peacock__pb2.SaveRefDataFromQC_Msg.SerializeToString,
                response_deserializer=peacock__pb2.NoneReply.FromString,
                )
        self.SaveStrategyConfig = channel.unary_unary(
                '/peacock.Peacock/SaveStrategyConfig',
                request_serializer=peacock__pb2.SaveStrategyConfig_Msg.SerializeToString,
                response_deserializer=peacock__pb2.SaveStrategyConfig_Reply.FromString,
                )
        self.GetStrategyConfig = channel.unary_unary(
                '/peacock.Peacock/GetStrategyConfig',
                request_serializer=peacock__pb2.GetStrategyConfig_Msg.SerializeToString,
                response_deserializer=peacock__pb2.GetStrategyConfig_Reply.FromString,
                )
        self.RemoveStrategyConfig = channel.unary_unary(
                '/peacock.Peacock/RemoveStrategyConfig',
                request_serializer=peacock__pb2.RemoveStrategyConfig_Msg.SerializeToString,
                response_deserializer=peacock__pb2.Dummy_Reply.FromString,
                )
        self.RemoveOldConfig = channel.unary_unary(
                '/peacock.Peacock/RemoveOldConfig',
                request_serializer=peacock__pb2.RemoveOldConfig_Msg.SerializeToString,
                response_deserializer=peacock__pb2.Dummy_Reply.FromString,
                )
        self.GetDataByStrategyId = channel.unary_unary(
                '/peacock.Peacock/GetDataByStrategyId',
                request_serializer=peacock__pb2.GetDataByStrategyId_Msg.SerializeToString,
                response_deserializer=peacock__pb2.GetDataByStrategyId_Reply.FromString,
                )
        self.GetTimeSeriesData = channel.unary_unary(
                '/peacock.Peacock/GetTimeSeriesData',
                request_serializer=peacock__pb2.GetTimeSeriesData_Msg.SerializeToString,
                response_deserializer=peacock__pb2.GetTimeSeriesData_Reply.FromString,
                )
        self.HealthCheck = channel.unary_unary(
                '/peacock.Peacock/HealthCheck',
                request_serializer=peacock__pb2.Ping.SerializeToString,
                response_deserializer=peacock__pb2.Pong.FromString,
                )


class PeacockServicer(object):
    """The greeting service definition.
    """

    def SaveFileToColud(self, request, context):
        """Unary - request and respond
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveRefDataPriceFromQC(self, request, context):
        """magpie - start
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveRefDataFromQC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveStrategyConfig(self, request, context):
        """magpie - end
        tweety - start
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStrategyConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveStrategyConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveOldConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataByStrategyId(self, request, context):
        """tweety - end
        eagle - start
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTimeSeriesData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
        """eagle - end
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PeacockServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaveFileToColud': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveFileToColud,
                    request_deserializer=peacock__pb2.SaveFileToColud_Msg.FromString,
                    response_serializer=peacock__pb2.NoneReply.SerializeToString,
            ),
            'SaveRefDataPriceFromQC': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveRefDataPriceFromQC,
                    request_deserializer=peacock__pb2.SaveRefDataPriceFromQC_Msg.FromString,
                    response_serializer=peacock__pb2.NoneReply.SerializeToString,
            ),
            'SaveRefDataFromQC': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveRefDataFromQC,
                    request_deserializer=peacock__pb2.SaveRefDataFromQC_Msg.FromString,
                    response_serializer=peacock__pb2.NoneReply.SerializeToString,
            ),
            'SaveStrategyConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveStrategyConfig,
                    request_deserializer=peacock__pb2.SaveStrategyConfig_Msg.FromString,
                    response_serializer=peacock__pb2.SaveStrategyConfig_Reply.SerializeToString,
            ),
            'GetStrategyConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStrategyConfig,
                    request_deserializer=peacock__pb2.GetStrategyConfig_Msg.FromString,
                    response_serializer=peacock__pb2.GetStrategyConfig_Reply.SerializeToString,
            ),
            'RemoveStrategyConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveStrategyConfig,
                    request_deserializer=peacock__pb2.RemoveStrategyConfig_Msg.FromString,
                    response_serializer=peacock__pb2.Dummy_Reply.SerializeToString,
            ),
            'RemoveOldConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveOldConfig,
                    request_deserializer=peacock__pb2.RemoveOldConfig_Msg.FromString,
                    response_serializer=peacock__pb2.Dummy_Reply.SerializeToString,
            ),
            'GetDataByStrategyId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataByStrategyId,
                    request_deserializer=peacock__pb2.GetDataByStrategyId_Msg.FromString,
                    response_serializer=peacock__pb2.GetDataByStrategyId_Reply.SerializeToString,
            ),
            'GetTimeSeriesData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTimeSeriesData,
                    request_deserializer=peacock__pb2.GetTimeSeriesData_Msg.FromString,
                    response_serializer=peacock__pb2.GetTimeSeriesData_Reply.SerializeToString,
            ),
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=peacock__pb2.Ping.FromString,
                    response_serializer=peacock__pb2.Pong.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'peacock.Peacock', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Peacock(object):
    """The greeting service definition.
    """

    @staticmethod
    def SaveFileToColud(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/SaveFileToColud',
            peacock__pb2.SaveFileToColud_Msg.SerializeToString,
            peacock__pb2.NoneReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveRefDataPriceFromQC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/SaveRefDataPriceFromQC',
            peacock__pb2.SaveRefDataPriceFromQC_Msg.SerializeToString,
            peacock__pb2.NoneReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveRefDataFromQC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/SaveRefDataFromQC',
            peacock__pb2.SaveRefDataFromQC_Msg.SerializeToString,
            peacock__pb2.NoneReply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/SaveStrategyConfig',
            peacock__pb2.SaveStrategyConfig_Msg.SerializeToString,
            peacock__pb2.SaveStrategyConfig_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStrategyConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/GetStrategyConfig',
            peacock__pb2.GetStrategyConfig_Msg.SerializeToString,
            peacock__pb2.GetStrategyConfig_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveStrategyConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/RemoveStrategyConfig',
            peacock__pb2.RemoveStrategyConfig_Msg.SerializeToString,
            peacock__pb2.Dummy_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveOldConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/RemoveOldConfig',
            peacock__pb2.RemoveOldConfig_Msg.SerializeToString,
            peacock__pb2.Dummy_Reply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/GetDataByStrategyId',
            peacock__pb2.GetDataByStrategyId_Msg.SerializeToString,
            peacock__pb2.GetDataByStrategyId_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTimeSeriesData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/GetTimeSeriesData',
            peacock__pb2.GetTimeSeriesData_Msg.SerializeToString,
            peacock__pb2.GetTimeSeriesData_Reply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/peacock.Peacock/HealthCheck',
            peacock__pb2.Ping.SerializeToString,
            peacock__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
