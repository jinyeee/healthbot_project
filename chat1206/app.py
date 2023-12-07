# 최초 코드

# from dotenv import load_dotenv
# import os
# from openai import OpenAI
# import streamlit as st
# import time

# load_dotenv()
# API_KEY = os.environ['OPENAI_API_KEY']

# client = OpenAI(api_key=API_KEY)

# #thread id를 하나로 관리하기 위함
# if 'thread_id' not in st.session_state:
#     thread = client.beta.threads.create()
#     st.session_state.thread_id = thread.id

# #thread_id, assistant_id 설정
# thread_id = st.session_state.thread_id
# #미리 만들어 둔 Assistant
# assistant_id = "asst_0ar0OMRRHitD465HbUtcbkPP"      

# #메세지 모두 불러오기
# thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

# #페이지 제목
# st.header("돌팔이01")

# #메세지 역순으로 가져와서 UI에 뿌려주기
# for msg in thread_messages.data:
#     with st.chat_message(msg.role):
#         st.write(msg.content[0].text.value)




# #입력창에 입력을 받아서 입력된 내용으로 메세지 생성
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

#     #RUN을 돌리는 과정
#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistant_id,
#     )

#     with st.spinner('응답 기다리는 중...'):
#         #RUN이 completed 되었나 1초마다 체크
#         while run.status != "completed":
#             time.sleep(1)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread_id,
#                 run_id=run.id
#             )

#     #while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
#     messages = client.beta.threads.messages.list(
#         thread_id=thread_id
#     )
#     #마지막 메세지 UI에 추가하기
#     with st.chat_message(messages.data[0].role):
#         st.write(messages.data[0].content[0].text.value)

# =====================================

# from dotenv import load_dotenv
# import os
# from openai import OpenAI
# import streamlit as st
# import time

# load_dotenv()
# API_KEY = os.environ['OPENAI_API_KEY']

# client = OpenAI(api_key=API_KEY)

# # Thread id를 하나로 관리하기 위함
# if 'thread_id' not in st.session_state:
#     thread = client.beta.threads.create()
#     st.session_state.thread_id = thread.id

# # thread_id, assistant_id 설정
# thread_id = st.session_state.thread_id
# # 미리 만들어 둔 Assistant
# assistant_id = "asst_0ar0OMRRHitD465HbUtcbkPP"      

# # 채팅을 시작할 때 "Hello, master." 메시지를 보내기
# if 'initialized' not in st.session_state:
#     # 초기 메시지 보내기
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content="1. 증상에 따른 예비진단(핵심 플로우)\n2. 주변 동네 병원을 소개(생략 후 바로 리뷰파트로)\n3. 건강잡담(의료정보 자유롭게 질의)"
#     )
#     st.session_state.initialized = True

# # 메세지 모두 불러오기
# thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

# # 페이지 제목
# st.header("돌팔이01")

# # 메세지 역순으로 가져와서 UI에 뿌려주기
# for msg in thread_messages.data:
#     with st.chat_message(msg.role):
#         st.write(msg.content[0].text.value)

# # 입력창에 입력을 받아서 입력된 내용으로 메세지 생성
# prompt = st.chat_input("착하게 살자!")
# if prompt:
#     message = client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=prompt
#     )

#     # 입력한 메세지 UI에 표시
#     with st.chat_message(message.role):
#         st.write(message.content[0].text.value)

#     # RUN을 돌리는 과정
#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistant_id,
#     )

#     with st.spinner('응답 기다리는 중...'):
#         # RUN이 completed 되었나 1초마다 체크
#         while run.status != "completed":
#             time.sleep(1)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread_id,
#                 run_id=run.id
#             )

#     # while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
#     messages = client.beta.threads.messages.list(
#         thread_id=thread_id
#     )
#     # 마지막 메세지 UI에 추가하기
#     with st.chat_message(messages.data[0].role):
#         st.write(messages.data[0].content[0].text.value)
  
# ==================================

# 이게 main
# 초기 안내문 나온다. 채팅 치면 초기 안내문 안 사라짐. 채팅이 누적되어 표시됨.
# st.session_state.greeting_displayed = True 이 부분으로 해결! 
# False면 안 나온다!


# from dotenv import load_dotenv
# import os
# from openai import OpenAI
# import streamlit as st
# import time

# # Load environment variables
# load_dotenv()
# API_KEY = os.environ['OPENAI_API_KEY']

# client = OpenAI(api_key=API_KEY)

# # Initialize session state for thread management
# if 'thread_id' not in st.session_state:
#     thread = client.beta.threads.create()
#     st.session_state.thread_id = thread.id

# # Assign thread_id and assistant_id
# thread_id = st.session_state.thread_id
# assistant_id = "asst_0ar0OMRRHitD465HbUtcbkPP"  # Your Assistant ID


# # Initialize session state for greeting message
# if 'greeting_displayed' not in st.session_state:
#     st.session_state.greeting_displayed = False

# # Function to display a greeting message from the assistant
# def display_greeting_message():
#     if not st.session_state.greeting_displayed:
#         greeting_text = "1. 증상에 따른 예비진단(핵심 플로우)\n2. 주변 동네 병원을 소개(생략 후 바로 리뷰파트로)\n3. 건강잡담(의료정보 자유롭게 질의)"
#         with st.chat_message("assistant"):  # Display as if it's from the assistant
#             st.write(greeting_text)
# #        st.session_state.greeting_displayed = True

# # Load and display existing messages
# thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

# st.header("돌팔이01")
# # Display the greeting message below the header
# display_greeting_message()


# for msg in thread_messages.data:
#     with st.chat_message(msg.role):
#         st.write(msg.content[0].text.value)

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

#     #RUN을 돌리는 과정
#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistant_id,
#     )

#     with st.spinner('응답 기다리는 중...'):
#         #RUN이 completed 되었나 1초마다 체크
#         while run.status != "completed":
#             time.sleep(1)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread_id,
#                 run_id=run.id
#             )

#     #while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
#     messages = client.beta.threads.messages.list(
#         thread_id=thread_id
#     )
#     #마지막 메세지 UI에 추가하기
#     with st.chat_message(messages.data[0].role):
#         st.write(messages.data[0].content[0].text.value)
        

        
        
# ========================================================

# main + embedding 추가 모델

from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time
import requests
import pandas as pd

# Load environment variables
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)




# # option - 1

# # Function to upload a file and create embeddings using text-embedding-ada-002 model
# def upload_file_and_create_embeddings(file_path, model="text-embedding-ada-002"):
#     # Upload the file
#     with open(file_path, 'rb') as file:
#         response = client.files.upload(file=file, purpose="embeddings")
#         file_id = response["id"]

#     # Create embeddings for the file using the specified model
#     response = client.embeddings.create(file_id=file_id, model=model)
#     embeddings_id = response["id"]
#     return file_id, embeddings_id

# # Example usage of the upload function
# file_path = r"C:\Users\user\Desktop\파프\asan_hospital_data.py"  # Replace with your file path
# file_id, embeddings_id = upload_file_and_create_embeddings(file_path)

# # Store the file ID and embeddings ID in session state for later use
# st.session_state.file_id = file_id
# st.session_state.embeddings_id = embeddings_id

# # Function to retrieve embeddings
# def retrieve_embeddings(embeddings_id):
#     response = client.embeddings.retrieve(embeddings_id)
#     return response["data"]

# # Example usage to retrieve embeddings
# embeddings = retrieve_embeddings(st.session_state.embeddings_id)




# # option - 2
# # Assuming your data is in a CSV file, replace 'your_data.csv' with your actual file path
# data_path = r"C:\path\to\your_data.csv"  # Use a raw string for the file path
# df = pd.read_csv(data_path)

# # Your existing code for adding embeddings
# df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))

# # Saving the DataFrame to a new CSV file
# output_path = r"C:\Users\user\Desktop\파프\아산병원데이터.csv"  # Corrected file path
# df.to_csv(output_path, index=False)





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

# Input for user's message
prompt = st.chat_input("착하게 살자!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    #입력한 메세지 UI에 표시
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

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
        
