from typing import Optional
from uagents import Model

class Message(Model):
    message: str
    type: Optional[str] = "message"