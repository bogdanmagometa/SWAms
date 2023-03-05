import uuid

class Message:
    def __init__(self, message_text: str, message_uuid):
        self._message_text = message_text
        self._uuid = message_uuid

    @property
    def uuid(self):
        return self._uuid

    @property
    def message_text(self):
        return self._message_text

    @classmethod
    def create_message_with_uuid(clas, message_text) -> 'Message':
        return clas(message_text, uuid.uuid1())
