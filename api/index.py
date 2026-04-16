import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

from middleware.middleware import setup_cors
from middleware.controller import voiceAgentController
from middleware.model import voiceAgent

app = FastAPI()
setup_cors(app)

@app.post("/chatbot/voice/")
async def rag(item: voiceAgent):
    try:
        response = voiceAgentController(item.base64, item.extension)
        return StreamingResponse(
            io.BytesIO(response),
            media_type="audio/mpeg"
        )
    except Exception as e:
        return {
            "error": str(e),
            "statusCode": 500
        }

@app.get("/")
def home():
    return {"message": "OK"}