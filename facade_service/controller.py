from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from service.service import FacadeService
from typing import List, Any

app = FastAPI()
logging_uri = 'http://localhost:8001/'
messages_uri = 'http://localhost:8083/'

facade_service = FacadeService(logging_uri, messages_uri)

@app.get("/", response_class=PlainTextResponse)
async def read_messages() -> List[str]:
    messages = await facade_service.read_messages()
    if messages is None:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse([msg.message_text for msg in messages])


@app.post("/")
async def add_message(message_text: str) -> Any:
    if not message_text:
        return HTTPException(status.HTTP_400_BAD_REQUEST)

    if facade_service.log_message(message_text):
        return HTTPException(status.HTTP_200_OK)
    return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
