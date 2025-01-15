from grpc.aio import insecure_channel

from clients.grpc.proto.line_provider.line_provider_pb2_grpc import LineProviderStub
from core.config import settings


class GRPCClient:
    def __init__(self):
        self.channel = insecure_channel(f"{settings.grpc_server.host}:{settings.grpc_server.port}")
        self.stub = LineProviderStub(self.channel)
        self.auth_token = f"Bearer {settings.grpc_server.auth_token}"
        self.metadata = [("authorization", self.auth_token)]

    async def get_available_events(self, request):
        return await self.stub.GetEvents(request, metadata=self.metadata)

    async def check_event_existing(self, request):
        return await self.stub.CheckIfEventExists(request, metadata=self.metadata)


grpc_client = GRPCClient()
