import asyncio
import json
from typing import Any, Dict
from fastapi import Response
from uagents.query import query
from agents.generation import generate_demographic
from agents.agent import create_agents
from uagents import Agent, Bureau, Context, Protocol, Model
from models.message import Message
from models.models import AgentInfoResponse, AgentState

AGE_DEMO_GROUPS = {
    "Under 25": {
        "population": 1,
        "median_income": "$95,000"
    },
    "25 - 44": {
        "population": 1,
        "median_income": "$195,000"
    },
    "45 - 65": {
        "population": 1,
        "median_income": "$130,000"
    },
    "Over 65": {
        "population": 1,
        "median_income": "$65,000"
    }
}

ZIPCODES_COORDS_INCOME = {
    111827: (37.73078,-122.38261), #94124
    115649: (37.77939,-122.41774), #94102
    116916: (37.79094,-122.40873), #94108
    141326: (37.80377,-122.41142), #94133
    142394: (37.72289,-122.41006), #94134
    143097: (37.79099,-122.40188), #94104
    146999: (37.72301,-122.48476), #94132
    147150: (37.82012,-122.36897), #94130
    158861: (37.77550,-122.41292), #94103
    162512: (37.72174,-122.44460), #94112
    167261: (37.79616,-122.42090), #94109
    179517: (37.76196,-122.48313), #94122
    187450: (37.78087,-122.49528), #94121
    201841: (37.74435,-122.48429), #94116
    215550: (37.78597,-122.43726), #94115
    222915: (37.79885,-122.39860), #94111
    223044: (37.74868,-122.41581), #94110
    226692: (37.76509,-122.39435), #94107
    227113: (37.78236,-122.46080), #94118
    242062: (37.76917,-122.44250), #94117
    244957: (37.77055,-122.39561), #94158
    254595: (37.75823,-122.43951), #94114
    259573: (37.74642,-122.44359), #94131
    274058: (37.79878,-122.46608), #94129
    285493: (37.73237,-122.45744), #94127
    300463: (37.80184,-122.43653), #94123
    347725: (37.78854,-122.39387), #94105
}

 
async def main():
    demographics = None
    while True:
        try: 
            demographics = await generate_demographic(AGE_DEMO_GROUPS, ZIPCODES_COORDS_INCOME)
            break
        except:
            pass
    print(demographics)
    agents = await create_agents(demographics)

    time = 0

    # define master agent
    master_agent = Agent(name='master')
    master_agent.storage.set("agent_addresses", [agent.address for agent in agents])
    master_agent.storage.set("agent_data", [
        dict({"address": agent.address, "coordinates": agent.storage.get("coordinates")}, **agent.storage.get("data"))
    for agent in agents])

    @master_agent.on_rest_get("/agents", AgentInfoResponse)
    async def get_all_agents_current_state(ctx: Context) -> Dict[str, Any]:
        return {"agents": master_agent.storage.get("agent_data")}

    # broadcast to all agents
    @master_agent.on_rest_post("/message", Message, Message)
    async def broadcast_to_agents(ctx: Context, req: Message) -> Message:
        for address in master_agent.storage.get("agent_addresses"):
            await ctx.send(address, Message(message=req.message, type="message"))
    
    @master_agent.on_rest_post("/step", Message, Message)
    async def step(ctx: Context, req: Message) -> Message:
        agent_states = []
        for address in master_agent.storage.get("agent_addresses"):
            await ctx.send(address, Message(message=req.message, type="step"))
        return Response(content="Success", status_code=200)

    @master_agent.on_message(model=AgentState, replies=Message)
    async def on_message(ctx: Context, sender: str, message: AgentState):
        for data in master_agent.storage.get("agent_data"):
            if data["address"] == sender:
                data.update(message.dict())

    bureau = Bureau(port=8000, endpoint='https://localhost:8000')
    bureau.add(master_agent)
    for agent in agents:
        bureau.add(agent)
        
    await bureau.run_async()

asyncio.run(main())