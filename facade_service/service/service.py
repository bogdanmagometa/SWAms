from domain.message import Message
from repository.repository import FacadeRepository
from typing import List, Optional
import asyncio

class FacadeService:
    def __init__(self, logging_uris: str, messaging_uri: str):
        self._repository = FacadeRepository(logging_uris, messaging_uri)

    def log_message(self, msg_text: str) -> bool:
        message = Message.create_message_with_uuid(msg_text)
        return self._repository.log_message(message)

    async def read_messages(self) -> Optional[List[Message]]:
        cor1 = self._repository.read_logged_messages()
        cor2 = self._repository.read_message()
        logged_messages, message_from_message_service = await asyncio.gather(cor1, cor2)

        if logged_messages is None or message_from_message_service is None:
            return None

        return [*logged_messages, Message(message_from_message_service, None)]
