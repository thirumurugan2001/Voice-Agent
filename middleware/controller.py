from helper.audioExtraction import audioExtraction
from helper.speechTranscription import SpeechTranscription
from helper.ConnectChatBot import ConnectChatBot
from helper.textToSpeech import text_to_speech
from helper.rag import similaritySearch

def voiceAgentController(base64,extension):
    try:
        if base64 != "":
            fileurl= audioExtraction(base64,extension)
            if fileurl:
                result = SpeechTranscription(fileurl)
                if result is None:
                    return {
                        "message":"Failed to transcribe audio !",
                        "statusCode":400,
                        "Status":False
                    }
                else :
                    knowledgeBaseData = similaritySearch(result)
                    chatbotResponse = ConnectChatBot(result,knowledgeBaseData)
                    text_to_speech_response = text_to_speech(chatbotResponse)
                    if chatbotResponse is None:
                        return {
                            "message":"Failed to get response from chatbot !",
                            "statusCode":400,
                            "Status":False
                        }
                    else :
                        if text_to_speech_response:
                            return text_to_speech_response
            else :  
                return {
                    "message":"Failed to extract audio !",
                    "statusCode":400,
                    "Status":False
                }
        else:
            return {
                "message":"Invalid data !",
                "statusCode":400,
                "Status":False
            }
    except Exception as e:
        print(f"Error in voiceAgentController controller.py file: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }