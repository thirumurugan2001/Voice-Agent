from Database.dbconnection import dbconnection
from helper.getEmbedding import get_embedding
from helper.ConnectChatBot import ConnectChatBot

# Function to get the most relevant answer from the database
def similaritySearch(Question):
    try:
        conn=dbconnection()
        cursor=conn.cursor()
        embedding = get_embedding(Question)
        select_query = """SELECT description, dot_product(vector, JSON_ARRAY_PACK("{0}")) AS score FROM About ORDER BY score DESC LIMIT 2 """.format(embedding)
        cursor.execute(select_query) 
        rows = cursor.fetchall() 
        conn.close()
        knowledgeBaseData=f"{rows[0][0]} and {rows[1][0]}"
        if rows:
            response = ConnectChatBot(Question,knowledgeBaseData)
            return {
                "data":response,
                "statusCode":200,
                "message":"Success",
                "Status":True
            }
        else:
            return {
                "statusCode":200,
                "status":False,
                "message":"No relevant information found in the database.",

            }
    except Exception as e:
        print(f"Error in rag function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }
