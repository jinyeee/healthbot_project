# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests

# app = FastAPI()

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat/")
# async def chat(chat_request: ChatRequest):
#     # Replace with the actual URL and logic to communicate with the Streamlit chatbot
#     chatbot_url = "http://localhost:8000/chat/"
#     response = requests.post(chatbot_url, json={"message": chat_request.message})
    
#     if response.status_code == 200:
#         return {"response": response.json()["reply"]}
#     else:
#         raise HTTPException(status_code=500, detail="Error communicating with chatbot")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Define the FastAPI app
app = FastAPI()

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Endpoint to handle chat requests
@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    try:
        # Logic to interact with OpenAI's GPT-3 and generate a response
        # Replace this with your actual logic for using OpenAI API
        # For example, using OpenAI's `Completion` API to get a response
        response = client.Completion.create(
            model="text-davinci-003",  # Replace with your desired model
            prompt=chat_request.message,
            max_tokens=150  # Adjust based on your requirements
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




