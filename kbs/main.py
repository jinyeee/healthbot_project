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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# OpenAI API key setup
#load_dotenv()
#API_KEY = os.environ['OPENAI_API_KEY']

# TODO api 키 로드 변경 및 링크 동적 생성 함수 추가
import json
with open('openai_key.json', 'r') as file:
    API_KEY = json.load(file)['OPENAI_API_KEY']
print('API_KEY', API_KEY)
client = OpenAI(api_key=API_KEY)
def next_page(part, gu):
    return f'http://localhost:8080/hospital/find?department={part}&location={gu}'
parts = ['내과', '이비인후과','치과']
def check_part( sentences ):
    for word in sentences.split():
        if word in parts:
            return (True, word)
    return (False,'')

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
# TODO 구정보 전달되도록 맴버 추가
class UserRequest(BaseModel):
    utterance: str
    gu: str

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
    user_question = user_request.utterance.strip()
    # TODO 구정보 추출 되도록 추가
    gu = user_request.gu.strip() #'강남구'
    logger.debug(f'Received POST request: {user_question}')

    if user_question:
        # TODO 구정보 전달
        gpt_answer = get_qa_by_gpt(user_question, gu)
        response_queue.append(gpt_answer)
        logger.debug(f'Response queue: {response_queue}')
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
# TODO 구정보 파라미터 추가
def get_qa_by_gpt(prompt, gu='', temperature=0.5, top_p=0.5, max_tokens=100, frequency_penalty=0.6, presence_penalty=0.1, stop=None, n=1):
    prompt_template = [
    {"role": "system", "content": """I am a good and kind medical assistant. 
     I will respond in Korean with answers of fewer than 50 words. If the user 
     provides their symptoms, gender, and age, I will provide three likely 
     medical conditions. When a user presents information about his or her symptoms, 
     “다른 증상은 없냥?” is asked only once in the entire conversation and must
     be answered in the following format. "당신의 증상과 건강상태를 고려하면 유력한 
     질병은 (질환명1) (0~100%), (질환명2) (0~100%), (질환명3) (0~100%) 일 가능성이 
     높습니다냥. 이에 따라 당신이 방문해야 할 진료과를 추천드리면 
     <질환명1과 관련한 진료과 목록>, <질환명2과 관련한 진료과 목록>, 
     <질환명3과 관련한 진료과 목록>입니다냥."`
     (Considering your symptoms and health, the likely diseases
     are (Disease 1) (0~100%), (Disease 2) (0~100%), (Disease 3) (0~100%).
     Accordingly, I recommend visiting <Specialty 1>, <Specialty 2>, 
     <Specialty 3>.) """},
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
        # TODO 구정보 테스트 
        # print( '유저 질문 -> ', prompt)
        logger.debug(f'GPT response: {message}')

        # TODO GPT응답에서 해당과 정보가 나오면 링크를 동적 생성해서 리턴
        print( check_part( message ) )
        flag, part = check_part( message )
        if flag:
            # URL 정보 생성 완료
            print( next_page(part,gu) )
        return message
    except Exception as e:
        logger.error(f'Error during OpenAI API call: {e}')
        return "Sorry, I am unable to process your request at the moment."