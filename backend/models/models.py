from typing import List, Dict
from uagents import Model

class AgentInfoResponse(Model):
    agents: List

class AgentState(Model):
    address: str
    coordinates: List
    name: str
    age: int
    income: int
    gender: str
    race: str
    occupation: str
    hobbies: List
    marital_status: str
    number_of_children: int
    home: List


class AgentStateResponse(Model):
    state: Dict
