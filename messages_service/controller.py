import os
from typing import List
import asyncio

from fastapi import FastAPI
import uvicorn
from hazelcast import HazelcastClient

from service import MessagesService
from domain import Message


app = FastAPI()
app.messages_service = MessagesService()
QUEUE_NAME = "messages_queue"

@app.get("/")
async def get_messages() -> List[Message]:
    messages = app.messages_service.get_all_messages()
    return messages

def poll_messages_queue():
    # print("Starting")
    hazelcast_client = HazelcastClient(cluster_members=["logging"], connection_timeout=30.0)
    messages_queue = hazelcast_client.get_queue(QUEUE_NAME)
    while True:
        # import time
        # time.sleep(1)
        # print("Ay")
        message = messages_queue.take().result()
        app.messages_service.add_message(message)

@app.on_event("startup")
async def app_startup():
    # asyncio.create_task(poll_messages_queue())
    asyncio.get_running_loop().run_in_executor(None, poll_messages_queue)

if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
