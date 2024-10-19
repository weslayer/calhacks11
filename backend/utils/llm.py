import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

async def generate_response(system: str, user: str = "", model: str="llama3-groq-8b-8192-tool-use-preview") -> str:
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
        max_tokens=8192,
        top_p=1,
        response_format={"type": ""}
    )
    
    return completion.choices[0].message.content
