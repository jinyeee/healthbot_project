# <main.py>
# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import ChatCompletion, OpenAI
from dotenv import load_dotenv
import logging
import os
import json

# #mongoDB 연결
# mongodb.py
from mongodb import insert_item_one, insert_item_many


#==========================================


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI models
class UserRequest(BaseModel):
    user_id: str # 사용자를 식별할 고유 ID
    utterance: str

class BotResponse(BaseModel):
    bot_message: str

# Queue object creation
response_queue = []

# Template directory setup
templates = Jinja2Templates(directory="templates")

# Root endpoint for rendering HTML
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chatbot endpoint
@app.post('/chatbot/', response_model=BotResponse)
async def chat(user_request: UserRequest):
    #user_id = user_request.user_id # 이거 어떻게 할지 고민 필요!
    user_question = user_request.utterance.strip()

    logger.debug(f'Received POST request: {user_question}')

    if user_question:
        gpt_answer = get_qa_by_gpt(user_question)
        response_queue.append(gpt_answer)
        logger.debug(f'Response queue: {response_queue}')

        # 여기에 진료과 뱉은 이후 추가 처리 부분 작성하면 됨
        # mongo db에 추가
        doc = insert_item_many(response_queue, db_name="HealthCube", collection_name='user_chat_logs')
        print(f"Data inserted with ID: {doc}")
        # 대화 기록 queue 초기화
        response_queue = []
        return JSONResponse(content={'bot_message': gpt_answer})
    else:
        return JSONResponse(content={'bot_message': 'No input received'})

# Additional endpoint to get the response
@app.get('/response/', response_class=JSONResponse)
async def get_response():
    if response_queue:
        return JSONResponse(content={'bot_message': response_queue.pop(0)})
    else:
        return JSONResponse(content={'bot_message': 'No response'})

# Function to get Q&A from GPT
def get_qa_by_gpt(prompt, temperature=0.5, top_p=0.5, max_tokens=100, frequency_penalty=0.6, presence_penalty=0.1, stop=None, n=1):
    prompt_template = [
    {"role": "system", "content":
    """
    You are a chatbot that gives guidance on which clinic the user has to visit giving a three expected illnesses, ordered by likelihood.
    Follow these steps:
    1. If user input their symptoms, complete the prompt as shown below:
    - user's symptom: soar throat with fever
    2. Tell them where to visit based on their symptoms in Korean, complete the prompt as shown below.
    Returns:
    <top 3 expected diseases and hospital departments you have to go>
    - 1. asthma - Paediatrics
    - 2. cold - Internal medicine department
    - 3. Chronic Obstructive Pulmonary Disease - Cardiology
    """

     }, # 프롬프트에 "" 넣으면 문자열로 인식
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            messages=prompt_template,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            n=n
        )

        message = response.choices[0].message.content
        logger.debug(f'GPT response: {message}')
        # ============ 시험
        # 진료과 추출
        specialty = extract_specialty_from_message(message)
        # JSON 형태로 변환
        specialty_json = json.dumps({"specialty": specialty})
        #==================
        return message, specialty_json

    except Exception as e:
        logger.error(f'Error during OpenAI API call: {e}')
        return "Sorry, I am unable to process your request at the moment."

# 진료과 추출 함수
def extract_specialty_from_message(message):

    specialties = message.split("-")[1:]
    specialties = [spec.strip() for spec in specialties]
    return specialties[0] # specialties에 ['내과','내과','내과'] 이렇게 들어갈듯

# def extract_specialty_from_message(message):
#     try:
#         # message에서 JSON 형태로 추출된 specialty_json을 파싱
#         parsed_message = json.loads(message)
#         # "specialty" 키에 해당하는 값 추출
#         specialty = parsed_message.get("specialty", [])
#         return specialty
#     except json.JSONDecodeError as e:
#         logger.error(f'Error decoding JSON from message: {e}')
#         return []

# 추가
doc = insert_item_many(response_queue, db_name= "HealthCube", collection_name='user_chat_logs')
print(f"Data inserted with ID: {inserted_id}")