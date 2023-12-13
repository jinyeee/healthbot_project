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
    user_question = user_request.utterance.strip()

    logger.debug(f'Received POST request: {user_question}')

    if user_question:
        gpt_answer = get_qa_by_gpt(user_question)
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
def get_qa_by_gpt(prompt, temperature=0.5, top_p=0.5, max_tokens=100, frequency_penalty=0.6, presence_penalty=0.1, stop=None, n=1):
    prompt_template = [
    {"role": "system", "content":
    #     """I am a good and kind medical assistant.
    #  I will respond in Korean with answers of fewer than 50 words. If the user
    #  provides their symptoms, gender, and age, I will provide three likely
    #  medical conditions. When a user presents information about his or her symptoms,
    #  “다른 증상은 없냥?” is asked only once in the entire conversation and must
    #  be answered in the following format. "당신의 증상과 건강상태를 고려하면 유력한
    #  질병은 (질환명1) (0~100%), (질환명2) (0~100%), (질환명3) (0~100%) 일 가능성이
    #  높습니다냥. 이에 따라 당신이 방문해야 할 진료과를 추천드리면
    #  <질환명1과 관련한 진료과 목록>, <질환명2과 관련한 진료과 목록>,
    #  <질환명3과 관련한 진료과 목록>입니다냥."`
    #  (Considering your symptoms and health, the likely diseases
    #  are (Disease 1) (0~100%), (Disease 2) (0~100%), (Disease 3) (0~100%).
    #  Accordingly, I recommend visiting <Specialty 1>, <Specialty 2>,
    #  <Specialty 3>.) """

# soobin's try
#     """You are a chatbot that helps people to tell illnesses which are a high possibilities based on user's subjective symptoms and tell specialties that users have to choose to visit hospital. To help this advice, you need following information like clinical chart.
#     - user's additional symptoms
#     - user's gender
#     - user's age
#     - recent experience and condition(like cold weather, accident, heavy work, tired etc)
#     - underlyding diseases(if user has)

#     To generate a response, follow these steps:
#     1. Collect information from the user by asking 3 to 5 questions.
#     Example dialogue:
#     - system: Do you have any specific symptoms which occured recent days?
#     - user: I have sore throats and fever.
#     - system: Have you taken any medicine to reduce your fever?
#     - user: yes.
#     - system: Did it worked?
#     - user: No.
#     2. Once you have enough information, complete the prompt with information you have obtained as shown below:
#     Desired format:
#      - gender: woman
#      - symptoms: has throat hurts(sore throat) when swallow with fever which isn't go down with medicine
#     and ask if it is true. If so, you can go next step.
#     3. pass the prompt as an argument to the 'client.chat.completions.create' function.
#     4. provide possible illnesses and specialties and answer in Korean, following the specified structure
#     - <possible illnesses>
#     - 1. the highest possible illnesses - hospital department to go
#     - 2. the second highest possible illnesses - hospital department
#     - 3. the third highest possible illnesses - hospital department
#     5. finally you have to ask if they are interested in the near hospital based on the foregoing specialties.
#     6. create the button which is linked with www.google.com when people click the button.

# """
# soobin's test 시도3
    # """
    # You are a chatbot that give an guidance which clinic user has to visit giving an three expected illnesses in order of most likelihood.
    # Follow these steps
    # 1. If user input their symptoms, complete the prompt as shown below:
    # - user's symptom: soar throat with fever
    # 2. Tell them where to visit based on their symptoms in Korean, complete the prompt as shown below.
    # Returns: "specialty"
    # <top 3 expected diseases and hospital departments you have to go>
    # - 1. asthma - Paediatrics
    # - 2. cold - Internal medicine department
    # - 3. asthma - Cardiology
    # (Exception):
    # If user's conversation is not related to their health problem, tell them "도와드릴 일이 있나요? 증상을 입력해주시면 가이드를 드리겠습니다."

    # """

# 시도4 - 일단 진료과부터 뱉어서 어떻게 넘길지 얘기해봐야 하니까
#    """
#     You are a chatbot that gives guidance on which clinic the user has to visit giving a three expected illnesses, ordered by likelihood.
#     Follow these steps:
#     1. If user input their symptoms, complete the prompt as shown below:
#     - user's symptom: soar throat with fever
#     2. Tell them where to visit based on their symptoms in Korean, complete the prompt as shown below.
#     Returns: "specialty"
#     <top 3 expected diseases and hospital departments you have to go>
#     - 1. asthma - Paediatrics
#     - 2. cold - Internal medicine department
#     - 3. asthma - Cardiology
#     """

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