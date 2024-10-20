import os
from dotenv import load_dotenv

load_dotenv()

KEYS = [
  os.environ.get("GROQ_API_KEY1"),
  os.environ.get("GROQ_API_KEY2"),
  os.environ.get("GROQ_API_KEY3"),
  os.environ.get("GROQ_API_KEY4"),
]

current = 0

def get_key():
  global current
  key = KEYS[current]
  current = (current + 1) % len(KEYS)
  return key