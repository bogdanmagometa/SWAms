from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from service.service import FacadeService
from typing import List, Any
import uvicorn
import os

app = FastAPI()
num_logging_services = int(os.getenv("NUM_LOGGING_SERVICES"))
logging_uri = f'http://{os.getenv("HOSTNAME_LOGGING")}:{os.getenv("PORT_LOGGING")}/'
messages_uri = f'http://{os.getenv("HOSTNAME_MESSAGES")}:{os.getenv("PORT_MESSAGES")}/'

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

    if not facade_service.log_message(message_text):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
