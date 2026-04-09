import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


def SpeechTranscription(audio_file_path: str) -> str:
    try :
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        if not os.path.exists(audio_file_path):
            return None
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3-turbo",
                temperature=0,
                response_format="verbose_json",
            )
        return transcription.text
    except Exception as e:
        print("Error in SpeechTranscription: ", str(e))
        return None