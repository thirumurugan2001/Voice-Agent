import os
import singlestoredb as s2
from dotenv import load_dotenv
load_dotenv()

# Function to connect to SingleStore
def dbconnection():
    try :
        conn = s2.connect( 
            host = os.getenv("DB_HOST"), 
            port = os.getenv("PORT"), 
            user =os.getenv("DB_USER"), 
            password = os.getenv("DB_PASSWORD") , 
            database =  os.getenv("DB_NAME")
        )
        print("Connected to SingleStore")
        return conn
    except Exception as e:
        print("Error in connecting to SingleStore: ", str(e))
        return None