import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def generate_response(message: str, prefill:str = "") -> str:
    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[
            {
                "role": "system",
                "content": message
            },
            {
                "role": "user",
                "content": prefill
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
    )
    return completion.choices[0].message.content
