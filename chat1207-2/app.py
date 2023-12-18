# 이게 main
# 초기 안내문 나온다. 채팅 치면 초기 안내문 안 사라짐. 채팅이 누적되어 표시됨.
# st.session_state.greeting_displayed = True 이 부분으로 해결! 
# False면 안 나온다!


# <app.py>
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time

# Load environment variables
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# Initialize session state for thread management
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# Assign thread_id and assistant_id
thread_id = st.session_state.thread_id
assistant_id = "asst_0ar0OMRRHitD465HbUtcbkPP"  # Your Assistant ID


# Initialize session state for greeting message
if 'greeting_displayed' not in st.session_state:
    st.session_state.greeting_displayed = False

# Function to display a greeting message from the assistant
def display_greeting_message():
    if not st.session_state.greeting_displayed:
        greeting_text = "1. 증상에 따른 예비진단(핵심 플로우)\n2. 주변 동네 병원을 소개(생략 후 바로 리뷰파트로)\n3. 건강잡담(의료정보 자유롭게 질의)"
        with st.chat_message("assistant"):  # Display as if it's from the assistant
            st.write(greeting_text)
#        st.session_state.greeting_displayed = True

# Load and display existing messages
thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

st.header("돌팔이01")
# Display the greeting message below the header
display_greeting_message()


for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)
        
        
# Input for user's message - 밑에서 수정
prompt = st.chat_input("착하게 살자!")
if prompt:
    # Sending the prompt to the Flask server
    response = requests.post("http://localhost:5000/process", json={"prompt": prompt})

    if response.status_code == 200:
        # Assuming the response contains the data you need
        flask_data = response.json()

        # Now use flask_data as needed
        # For example, display it in your Streamlit app
        with st.chat_message("response"):
            st.write(flask_data)
        
        
# # Input for user's message
# prompt = st.chat_input("착하게 살자!")
# if prompt:
#     message = client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=prompt
#     )

#     #입력한 메세지 UI에 표시
#     with st.chat_message(message.role):
#         st.write(message.content[0].text.value)

    #RUN을 돌리는 과정
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    with st.spinner('응답 기다리는 중...'):
        #RUN이 completed 되었나 1초마다 체크
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    #while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    #마지막 메세지 UI에 추가하기
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
        