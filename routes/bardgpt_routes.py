from fastapi import APIRouter
import os
import requests
from models.bardgpt_models import BardModel
from dotenv import load_dotenv
from bardapi import Bard

load_dotenv()

bardgpt_api_router = APIRouter()

@bardgpt_api_router.get('/')
async def get_index():

    return {
        "status": 200,
        "response": "Hello this is just a API named BardGPT"
    }
    
    
@bardgpt_api_router.post('/bard')
async def post_bard_response(data: BardModel):
    token = os.getenv('COOKIE')
    bard = Bard(token=token)
    data = data.dict()
    
    input_text = data["question"]
    response = bard.get_answer(input_text)['content']

    return {
        "status": 200,
        "response": response
    }
    
    
@bardgpt_api_router.post('/chatgpt')
async def post_bard_response(data: BardModel):
    API_KEY = os.getenv('API_KEY')
    URL = os.getenv('URL')
    
    data = data.dict()
    
    auth = f'Bearer {API_KEY}'
    
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }
    
    question = data["question"]
    prompt = f'Human: {question}'

    json_data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 0.7,
        'max_tokens': 256,
        'stop': [
            'Human:',
            'AI:',
        ],
    }
    
    response = requests.post(URL, headers=headers, json=json_data)
    
    # HTML template with JavaScript code
    html_content = f"""
        <html>
        <head>
            <script>
                console.log("{response.text}");
            </script>
        </head>
        <body>
        </body>
        </html>
    """
    
    res = response.json()
    
    ans_text = res["choices"][0]["text"]
    
    answer = ans_text
    
    if "\n\nRobot: " in ans_text:
        answer = ans_text.split("\n\nRobot: ")[1]

    return {
        "status": 200,
        "response": answer
    }