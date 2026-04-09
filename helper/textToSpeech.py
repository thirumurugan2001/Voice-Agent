import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.errors import UnprocessableEntityError
load_dotenv() 


def text_to_speech(text: str) -> bytes:
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")    
    if len(text.strip()) < 10:
        raise ValueError("Text must be at least 10 characters long")    
    try:
        client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        audio_bytes = b"".join(audio_stream)
        return audio_bytes    
    except UnprocessableEntityError:
        raise RuntimeError("ElevenLabs rejected the text input")
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {str(e)}")