# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import balanceador_pb2 as balanceador__pb2


class DataStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Server = channel.unary_unary(
                '/problema2_1.Data/Server',
                request_serializer=balanceador__pb2.ReqServer.SerializeToString,
                response_deserializer=balanceador__pb2.ResServer.FromString,
                )


class DataServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Server(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Server': grpc.unary_unary_rpc_method_handler(
                    servicer.Server,
                    request_deserializer=balanceador__pb2.ReqServer.FromString,
                    response_serializer=balanceador__pb2.ResServer.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'problema2_1.Data', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Data(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Server(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/problema2_1.Data/Server',
            balanceador__pb2.ReqServer.SerializeToString,
            balanceador__pb2.ResServer.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
