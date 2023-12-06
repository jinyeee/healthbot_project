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

# =========================================


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# import openai
# import os

# load_dotenv()
# API_KEY = os.getenv('OPENAI_API_KEY')

# if not API_KEY:
#     raise Exception("OPENAI_API_KEY not found in environment variables")

# openai.api_key = API_KEY

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat/")
# async def chat(request: ChatRequest):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or any other suitable model
#             messages=[{"role": "system", "content": "You are a helpful assistant."},
#                       {"role": "user", "content": request.message}]
#         )
#         return {"response": response.choices[0].message["content"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    
# =========================



from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv # API 키를 불러오기

import os
import openai

# .env 파일 로드
load_dotenv()

app = FastAPI()

# OpenAI API 키 설정
API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = API_KEY # 직접 openai 모듈의 api_key 속성에 할당

# HTML 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 루트 엔드포인트, HTML 페이지 렌더링
@app.get("/chatbot", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 챗봇 엔드포인트
@app.post("/chatbot/")
async def chatbot(message: str = Form(...)):
    try:
        # OpenAI API를 통해 대화 생성
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # OpenAI 엔진 선택
            prompt=message,
            max_tokens=1500 # 생성된 텍스트의 최대 토큰 수
        )
        reply = response.choices[0].text.strip()
        return {"message": reply}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
# OPTIONS 요청에 대한 처리
@app.options("/chat/")
async def options_chat():
    return {}





