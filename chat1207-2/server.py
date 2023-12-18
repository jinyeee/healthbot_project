# <server.py>

import openai
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import asyncio

app = Flask(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = API_KEY

async def fetch_completion(prompt):
    from openai import AsyncOpenAI
    async_client = AsyncOpenAI()
    response = await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.json
        prompt = data.get("prompt")
        
        # Run the async function and wait for completion
        response = asyncio.run(fetch_completion(prompt))
        
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in processing: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




# ======================================


# import openai
# from flask import Flask, request, jsonify
# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# app = Flask(__name__)

# # Load environment variables
# load_dotenv()
# API_KEY = os.environ['OPENAI_API_KEY']
# client = OpenAI(api_key=API_KEY)


# @app.route('/process', methods=['POST'])
# def process_request():
#     try:
#         data = request.json
#         prompt = data.get("prompt")
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or another model of your choice
#             messages=[{"role": "system", "content": "Your system message here (if any)"},
#                       {"role": "user", "content": prompt}]
#         )
#         return jsonify(response)
#     except Exception as e:
#         app.logger.error(f"Error in processing: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
    
    
    
    












# @app.route('/process', methods=['POST'])
# def process_request():
#     data = request.json
#     # You will need to extract the necessary information from the data
#     # and then use it to interact with the OpenAI API or perform other logic

#     # Example: Sending a request to OpenAI API
#     response = client.create_completion(...)  # replace with actual method to send request

#     # Process the response and return it
#     return jsonify(response)
