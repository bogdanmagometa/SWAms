from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
import os

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def get_messages():
    return "Not implemented yet"

if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is None:
        print("Error: port is not specified")
    else:
        port = int(port)
        uvicorn.run(app, host="0.0.0.0", port=port)
