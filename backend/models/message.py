from pydantic import BaseModel


class Message(BaseModel):
    type: str # update | agent
    message: str