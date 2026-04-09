import base64
import tempfile
from typing import Optional


def audioExtraction(base64_audio: str,suffix: Optional[str] = ".wav") -> str:
    try :
        if not base64_audio:
            raise None
        if "," in base64_audio:
            base64_audio = base64_audio.split(",")[1]
        audio_bytes = base64.b64decode(base64_audio)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        print(f"Audio file extracted and saved to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"Error in audioExtraction function audioExtraction.py file: {str(e)}")
        return None
