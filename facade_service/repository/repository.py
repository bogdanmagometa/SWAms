from domain.message import Message
import requests
import asyncio
import random
from typing import Optional, List
import json

class FacadeRepository:
    def __init__(self, logging_uris: str, messaging_uri: str):
        self._logging_uris = logging_uris
        self._messaging_uri = messaging_uri

    def log_message(self, message: Message) -> bool:
        message_json = json.dumps({"uuid": str(message.uuid), "text": message.message_text})
        response = requests.post(self._get_random_logging_uri(), data=message_json)
        return response.status_code == 200

    async def read_logged_messages(self) -> Optional[List[Message]]:
        response = requests.get(self._get_random_logging_uri())
        if response.status_code == 200:
            return [Message(message_text, None) for message_text in response.json()]
        return None

    async def read_message(self) -> Optional[str]:
        response = requests.get(self._messaging_uri)
        if response.status_code == 200:
            return response.text

    def _get_random_logging_uri(self) -> str:
        return random.choice(self._logging_uris)
