import os
from typing import List

from fastapi import FastAPI
import uvicorn
from hazelcast import HazelcastClient

from service import MessagesService
from domain import Message


app = FastAPI()
app.messages_service = MessagesService()
QUEUE_NAME = "messages_queue"

@app.get("/", response_class=List[Message])
async def get_messages():
    messages = app.messages_service.get_all_messages()
    return messages

@app.on_event("startup")
def poll_message_queue():
    hazelcast_client = HazelcastClient()
    messages_queue = hazelcast_client.get_queue(QUEUE_NAME).blocking()
    while True:
        message = messages_queue.take()
        app.messages_service.add_message(message)

if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
