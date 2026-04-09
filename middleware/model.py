from pydantic import BaseModel
from pydantic import Field as field

class voiceAgent(BaseModel): 
    base64: str = field(..., example="data:audio/ogg;base64,T2dnUwACAAAAAAAAAA...")
    extension: str = field(..., example=".wav")