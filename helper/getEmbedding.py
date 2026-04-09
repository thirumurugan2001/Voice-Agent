import os
from dotenv import load_dotenv
import cohere
load_dotenv()

# Function to get the embedding of the text
def get_embedding(text):
    try:
        token = os.getenv("COHERE_API_KEY")
        co = cohere.Client(token)  
        embedding = co.embed(
            model='embed-english-v3.0', 
            input_type='classification', 
            texts=[text]
            ).embeddings[0] 
        return embedding
    except Exception as e:
        print("Error in getting embedding: ", str(e))
        return None