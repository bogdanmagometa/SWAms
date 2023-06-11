from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from service.service import FacadeService
from typing import List, Any
import uvicorn
import os
import consul
import socket

app = FastAPI()
num_logging_services = int(os.getenv("NUM_LOGGING_SERVICES"))
logging_uri = f'http://{os.getenv("HOSTNAME_LOGGING")}:{os.getenv("PORT_LOGGING")}/'
messages_uri = f'http://{os.getenv("HOSTNAME_MESSAGES")}:{os.getenv("PORT_MESSAGES")}/'
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
    _, data1 =  consul_client.kv.get("logging_uri")
    _, data2 =  consul_client.kv.get("messages_uri")
    return data1['Value'].decode(), data2['Value'].decode()

register_with_consul("facade", int(port))
logging_uri, messages_uri = get_configuration()


facade_service = FacadeService(logging_uri, messages_uri)

@app.get("/", response_class=PlainTextResponse)
async def read_messages() -> List[str]:
    messages = await facade_service.read_messages()
    if messages is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse([msg.message_text for msg in messages])


@app.post("/")
async def add_message(message_text: str) -> Any:
    if not message_text:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if not await facade_service.add_message(message_text):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)



if __name__ == "__main__":
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
