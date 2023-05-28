class MessagesService:
    def __init__(self):
        self._messages = []

    def add_message(self, message):
        self._messages.append(message)

    def get_all_messages(self):
        return self._messages
