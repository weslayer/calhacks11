import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

clients=[
  Groq(api_key=os.environ.get("GROQ_API_KEY1")),
  Groq(api_key=os.environ.get("GROQ_API_KEY2")),
  Groq(api_key=os.environ.get("GROQ_API_KEY3")),
  Groq(api_key=os.environ.get("GROQ_API_KEY4")),
]

client_num = 0

def get_client():
    global client_num
    client = clients[client_num]
    client_num = (client_num + 1) % len(clients)
    return client

async def generate_response(system: str, user: str = "", model: str="llama-3.2-3b-preview") -> str:
    completion = get_client().chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    
    return completion.choices[0].message.content
