import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Simple in-memory cache
cache = {}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# OpenAI API key setup
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

# FastAPI app setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI models
class UserRequest(BaseModel):
    utterance: str
    gu: str

class BotResponse(BaseModel):
    bot_message: str
    department: str


# app.mount("/static", StaticFiles(directory="static"), name="static")

# Queue object creation
response_queue = []

# Template directory setup
templates = Jinja2Templates(directory="templates")

# Maximum number of previous exchanges to keep
MAX_HISTORY_LENGTH = 7

# Function to trim the conversation history
def trim_conversation_history():
    global response_queue
    if len(response_queue) > MAX_HISTORY_LENGTH:
        # Keep only the last MAX_HISTORY_LENGTH exchanges
        response_queue = response_queue[-MAX_HISTORY_LENGTH:]

# Root endpoint for rendering HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

# Chatbot endpoint
@app.post('/chatbot/', response_model=BotResponse)
async def chat(user_request: UserRequest):
    user_question = user_request.utterance.strip()
    gu = user_request.gu.strip()

    logger.debug(f'Received POST request: {user_question}')

    if user_question:
        # Call trim function before appending new response to ensure the queue length is maintained
        trim_conversation_history()

        gpt_answer, department = get_qa_by_gpt(user_question, gu)
        
        # Append individual turns to the response_queue
        response_queue.append({"role": "user", "content": user_question})
        response_queue.append({"role": "assistant", "content": gpt_answer})

        # Print the content of the objects for debugging
        print("User question:", user_question)
        print("GPT Answer:", gpt_answer)
        print("Department:", department)
        print("Response Queue:", response_queue)
        
        return JSONResponse(content={'bot_message': gpt_answer, 'department': department, 'gu': gu})
    else:
        return JSONResponse(content={'bot_message': 'No input received', 'department': '', 'gu': ''})


# Additional endpoint to get the response
@app.get('/response/', response_class=JSONResponse)
async def get_response():
    if response_queue:
        return JSONResponse(content={'bot_message': response_queue.pop(0)})
    else:
        return JSONResponse(content={'bot_message': 'No response', 'department': ''})

# Function to get Q&A from GPT
def get_qa_by_gpt(prompt, gu, temperature=0.5, top_p=0.5, max_tokens=100, frequency_penalty=0.6, presence_penalty=0.1, stop=None, n=1):
    # Build conversation history
    conversation_history = [
        {"role": "system", "content": """Your system content here"""},  # Add your system content
        {"role": "user", "content": prompt}
    ]
    
    for turn in response_queue:
        conversation_history.append(turn)

    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            messages=conversation_history,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            n=n
        )

        message = response.choices[0].message.content
        department = extract_department_from_message(message)

        logger.debug(f'GPT response: {message}')
        return message, department
    except Exception as e:
        logger.error(f'Error during OpenAI API call: {e}')
        return "Sorry, I am unable to process your request at the moment.", None


# Function to extract department from the GPT response
def extract_department_from_message(message):
    # Check if any medical department is mentioned in the bot's response
    for department in ["이비인후과", "내과", "치과"]:
        if department in message:
            return department
    return ''