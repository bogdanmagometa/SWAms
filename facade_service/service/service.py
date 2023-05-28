from domain.message import Message
from repository.repository import FacadeRepository
from typing import List, Optional
import asyncio
from hazelcast import HazelcastClient

QUEUE_NAME = "messages_queue"

class FacadeService:
    def __init__(self, logging_uri: str, messaging_uri: str):
        self._repository = FacadeRepository(logging_uri, messaging_uri)

        self._hazelcast_client = HazelcastClient()
        self._messages_queue = self._hazelcast_client.get_queue(QUEUE_NAME)

    async def add_message(self, msg_text: str) -> bool:
        message = Message.create_message_with_uuid(msg_text)
        queue_fut = self._messages_queue.put(message)
        repository_fut = self._repository.log_message(message)
        _, status = await asyncio.gather(queue_fut, repository_fut)
        return status

    async def read_messages(self) -> Optional[List[Message]]:
        cor1 = self._repository.read_logged_messages()
        cor2 = self._repository.read_messages()
        logged_messages, messages = await asyncio.gather(cor1, cor2)

        if logged_messages is None or messages is None:
            return None

        return logged_messages + messages
