import asyncio

from google.protobuf.json_format import MessageToDict

from tests.client.test_client import grpc_client
from tests.client.test_request import check_event_request


def test_GRPCAsyncServerCheckEvent():
    result = asyncio.get_event_loop().run_until_complete(grpc_client.check_event_existing(check_event_request))
    assert isinstance(result, object)
    print(f"Result: {MessageToDict(result)}")
