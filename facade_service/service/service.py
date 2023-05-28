from domain.message import (
    Message,
    MessageFactory
)
from repository.repository import FacadeRepository
from typing import List, Optional
import asyncio
from hazelcast import HazelcastClient
import time

QUEUE_NAME = "messages_queue"
HAZELCAST_NODE = "logging"

class FacadeService:
    def __init__(self, logging_uri: str, messaging_uri: str):
        self._repository = FacadeRepository(logging_uri, messaging_uri)

        self._hazelcast_client = HazelcastClient(cluster_members=[HAZELCAST_NODE], connection_timeout=30.0)
        self._messages_queue = self._hazelcast_client.get_queue(QUEUE_NAME)

    async def add_message(self, msg_text: str) -> bool:
        message = MessageFactory.build(message_text=msg_text)
        print("Received message " + message.json())
        queue_fut = self._messages_queue.put(message)
        repository_fut = self._repository.log_message(message)
        queue_fut.result()
        return await repository_fut

    async def read_messages(self) -> Optional[List[Message]]:
        cor1 = self._repository.read_logged_messages()
        cor2 = self._repository.read_messages()
        logged_messages, messages = await asyncio.gather(cor1, cor2)

        if logged_messages is None or messages is None:
            return None

        return logged_messages + messages
