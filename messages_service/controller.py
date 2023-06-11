import os
from typing import List
import asyncio

from fastapi import FastAPI
import uvicorn
from hazelcast import HazelcastClient
import consul
import socket

from service import MessagesService
from domain import Message


app = FastAPI()
app.messages_service = MessagesService()

port = os.getenv("PORT")

def register_with_consul(service_name, port):
    consul_client = consul.Consul("consul")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    consul_client.agent.service.register(
        name=service_name,
        service_id=f'{service_name}-{hostname}',
        address=ip_address,
        port=port,
    )

def get_configuration():
    consul_client = consul.Consul("consul")
    _, data1 =  consul_client.kv.get("queue_name")
    _, data2 =  consul_client.kv.get("hazelcast_node")
    return data1['Value'].decode(), data2['Value'].decode()

register_with_consul("messages", int(port))
QUEUE_NAME, HAZELCAST_NODE = get_configuration()

@app.get("/")
async def get_messages() -> List[Message]:
    messages = app.messages_service.get_all_messages()
    return messages

def poll_messages_queue():
    hazelcast_client = HazelcastClient(cluster_members=[HAZELCAST_NODE], connection_timeout=30.0)
    messages_queue = hazelcast_client.get_queue(QUEUE_NAME).blocking()
    while True:
        message = messages_queue.take()
        app.messages_service.add_message(message)

@app.on_event("startup")
async def app_startup():
    asyncio.get_running_loop().run_in_executor(None, poll_messages_queue)

if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
