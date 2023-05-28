from domain.message import Message
import requests
import asyncio
import random
from typing import Optional, List
import json
from pydantic.tools import parse_obj_as

class FacadeRepository:
    def __init__(self, logging_uri: str, messaging_uri: str):
        self._logging_uri = logging_uri
        self._messaging_uri = messaging_uri

    async def log_message(self, message: Message) -> bool:
        message_json = json.dumps({"uuid": str(message.uuid), "text": message.message_text})
        response = requests.post(self._get_next_logging_uri(), data=message_json)
        return response.status_code == 200

    async def read_logged_messages(self) -> Optional[List[Message]]:
        response = requests.get(self._get_next_logging_uri())
        if response.status_code == 200:
            return [parse_obj_as(Message, message) for message in response.json()]
        return None

    async def read_messages(self) -> Optional[str]:
        response = requests.get(self._messaging_uri)
        if response.status_code == 200:
            messages = [parse_obj_as(Message, message) for message in response.json()]
            return messages

    def _get_next_logging_uri(self) -> str:
        return self._logging_uri
