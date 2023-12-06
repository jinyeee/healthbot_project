from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

file = client.files.create(
  file=open("아산병원데이터.xlsx", "rb"),
  purpose="assistants"
)
print(file)
# file-ZS4L6QQ4fmc37MRynXIBDZPj

files = client.files.list()
print(files)