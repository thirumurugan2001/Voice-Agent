# from fastapi import FastAPI
# from middleware.middleware import setup_cors
# from middleware.controller import voiceAgentController
# app = FastAPI()
# setup_cors(app)
# from middleware.model import voiceAgent
# from fastapi.responses import StreamingResponse
# import io

# @app.post("/chatbot/voice/")
# async def rag(item: voiceAgent):
#     try:
#         response = voiceAgentController(item.base64,item.extension)
#         return StreamingResponse(
#             io.BytesIO(response),
#             media_type="audio/mpeg"
#         )
#     except Exception as e:
#         return {
#             "error": str(e),
#             "statusCode": 500
#         }

# @app.get("/")
# def home():
#     return {"message": "OK"}
    
# # python -m uvicorn main:app --reload


from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from middleware.middleware import setup_cors
from middleware.model import voiceAgent

app = FastAPI()
setup_cors(app)

@app.post("/chatbot/voice/")
async def rag(item: voiceAgent):
    try:
        file_path = r"Testing.mpeg"

        def iterfile():
            with open(file_path, "rb") as file:
                yield from file

        return StreamingResponse(
            iterfile(),
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
