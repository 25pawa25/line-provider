from functools import lru_cache

from grpc.aio import AioRpcError, insecure_channel
from loguru import logger

from clients.grpc.proto.bet import bet_pb2
from clients.grpc.proto.bet.bet_pb2_grpc import BetStub
from common.exceptions.grpc import GRPCConnectionException
from core.config import settings
from repository.interfaces.grpc.abc_bet_repository import AbstractBetRepository


class GRPCBetRepository(AbstractBetRepository):
    def __init__(self):
        self.metadata = settings.bet_grpc.metadata

    @property
    def channel(self):
        return insecure_channel(settings.bet_grpc.url)

    @property
    def stub(self):
        return BetStub(self.channel)

    async def update_event(self, event_id: str, status: str):
        """
        Update bets
        Args:
            event_id: id of the event
            status: status of the event
        """
        try:
            logger.info(f"Updating bets by event: {event_id}")
            await self.stub.UpdateBets(
                bet_pb2.UpdateBetsRequest(event_id=event_id, status=status),
                metadata=self.metadata,
            )
        except AioRpcError as e:
            logger.error(f"Error while updating bets: {e}")
            raise GRPCConnectionException(
                "Error while updating bets", event_id=event_id
            )


@lru_cache()
def get_grpc_bet_repository() -> AbstractBetRepository:
    return GRPCBetRepository()
