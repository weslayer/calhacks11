import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY1"))

async def generate_response(system: str, user: str = "", model: str="llama-3.2-3b-preview") -> str:
    completion = client.chat.completions.create(
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
