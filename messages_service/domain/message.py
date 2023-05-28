import uuid
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pydantic_factories import ModelFactory, Require, Use


class Message(BaseModel):
    message_text: str
    uuid: UUID


class MessageFactory(ModelFactory):
    __model__ = Message

    message_text = Require()
    uuid = uuid.uuid1

