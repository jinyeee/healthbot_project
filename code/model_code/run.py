# 기본 설정, 모듈가져오기, openai API KEY 세팅
#
import openai
from openai import OpenAI
import json
import os
import time
import queue as q # 자료구조, 큐, 요청을 차곡차곡 쌓아서 하나씩 꺼내서 처리




# 사전 정보 받기 필요
# 들어가면 질문 먼저 하기? '어디가 불편하신가요?'

def get_openai_key():
    key = None
    try:
        # openai_key.json 파일을 읽어서 "OPENAI_API_KEY" 키값 획득
        key_path = 'D:\SxS\파이널프로젝트\model_code\\openai_key.json'
        with open(key_path) as f:
            data = json.load(f)
            #print( data['OPENAI_API_KEY'][:5] )
        key = data['OPENAI_API_KEY']
    except Exception:
        # AWS Lambda의 환경변수
        key = os.environ['OPENAI_API_KEY']
    return key

# openAI 객체 생성
client = OpenAI(
    api_key = get_openai_key()
)

# 미리 입력받을 값을 설정
#"입력할 증상에 대하여 예측되는 질병,진료과에 대해 말해주세요. 이를 위해 사전에 질문을 (x5개 이상x-안 함) 진행해주세요"
# 비회원인 경우 = 회원 성별, 나이
pre_input_prompt = """You are a chatbot that helps to tell illnesses which have a high possibilities based on user's subjective symptoms and tell specialties that users have to choose to visit hospital. To help this advice, you need following information like clinical chart .
- user's symptoms
- user's gender
- age
- recent experience like cold weather, accident, heavy work, tired etc
- if user has underlying diseases get them

To create an answer, the process is as follows:
1. Collect information from the user by asking several questions.
2. Once you have enough information, check if the information is correct by complete the prompt. If it is true, go next step while if it's not, ask correct information again.
3. pass the prompt as an argument to call the 'generate_response' function.
4. you must tell possible illnesses and specialty and answer in Korean and prompt must be in English.
5. answer must be follow the structure as shown below
- <possible illnesses>
- 1. the highest possible illnesses - hospital department
- 2. the second highest possible illnesses - hospital department
- 3. the third highest possible illnesses - hospital department

"""

# 초기 프롬프트 설정
#conversation_history = [pre_input]

# def generate_response(prompt):
#     # 대화 기록과 현재 진행중인 프롬프트를 결합
#     #prompt_with_history = "\n".join(conversation_history + [prompt])

#     # openai api를 호출하여 응답 생성
#     response = openai.Completion.create(
#         engine = "gpt-3.5-turbo",   # gpt-4????? 후에 써보는 수도 있음"
#         #prompt = prompt_with_history,
#         temperatrue = 0.5,
#         max_tokens = 150 # 설정값!!!!!! 후에 조정
#         #stop =  # 출력값에 설정한 진료과 중 하나가 포함되어 있을때 대화 종료
#     )

user_prompt = "살이 갑자기 빠지고 근육통이 있어 어떤 진료과에 가야할까?"

# openai api를 호출하여 응답 생성
completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",   # gpt-4????? 후에 써보는 수도 있음"
    messages = [
        {"role":"system", "content" : pre_input_prompt},
        {"role":"user", "content": user_prompt}
    ],
    #prompt = prompt_with_history,
    temperatrue = 0.5,
    max_tokens = 150, # 설정값!!!!!! 후에 조정
    #stop =  # 출력값에 설정한 진료과 중 하나가 포함되어 있을때 대화 종료

)
# 생성된 응답 획득
generated_text = completion.choices[0]["message"]["content"].strip()

# 대화 기록 업데이트

# 큐 객체 생성
response_queue = q.Queue() # 응답결과를 담고 있는 큐

# GPT 답변 -> 채팅 메시지 구성, 서버 전달
# SimpleText 채팅 메세지 구성
# GPT 답변 -> 질의응답 텍스트
text_response_json_format = lambda msg:{
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": msg
                }
            }
        ]
    }
}

# GPT 텍스트 질문과 답변
def get_qa_by_gpt( prompt ):
    # 채팅형, 페르소나 부여, gpt-3.5-turbo, 응답메시지 리턴
    # 실습(저수준 openai api사용)
    prompt_template = [
        {
            # 페르소나 부여
            'role':'system',
            # 영어로 부여
            'content':'You are a thoughtful assistant. Respond to all input with specialty, four possible illnesses and answer in korean'
        },
        {
            'role':'user',
            'content': prompt
        }
    ]
    global client
    print('GPT 요청')
    # 지연시간 발생
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = prompt_template
    )
    message = response.choices[0].message.content
    print('GPT 응답', message)
    return message