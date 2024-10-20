import json
import random
import string
from utils.llm import generate_response
import asyncio
from uagents import Agent, Context
from models.message import Message
from models.models import AgentState
from yelp.yelp import getNearbyPlaces

def extract_keys(objects, keys):
    return [{key: obj[key] for key in keys if key in obj} for obj in objects]


async def create_agent(personal_info, port):

    agent = Agent(
        name=personal_info["name"], 
        port=port,
        seed=random.choice(string.ascii_letters)
    )

    # Get schedule string from LLM response
    schedule = await generate_response(
        system=f'''
        Generate a daily schedule for a person with these character traits: {str(personal_info)}. 
        Please try to represent each person as best as possible, taking into account every metric. Return your output as in ONLY strictly JSON format. Do not include plaintext.
        Here is an example schema:
            {{
                "7 am - 8 am": {{
                    "activity": "getting ready",
                    "location": "home"
                }},
                "8 am - 12 pm": {{
                    "activity": "working",
                    "location": "work"
                }},
                "12 pm - 1 pm": {{
                    "activity": "eating",
                    "location": "restaurant"
                }},
                "1 pm - 5 pm": {{
                    "activity": "working",
                    "location": "work"
                }},
                "5 pm - 7 pm": {{
                    "activity": "eating",
                    "location": "restaurant"
                }},
                "7 pm - 10 pm": {{
                    "activity": "resting",
                    "location": "home"
                }},
            }}
        '''
    )

    agent.storage.set('data', personal_info)
    agent.storage.set('coordinates', personal_info['home'])
    agent.storage.set('history', [])
    agent.storage.set('schedule', schedule)


    @agent.on_message(model=Message, replies=Message)
    async def on_message(ctx: Context, sender: str, message: Message):
        print(f"{agent.address} has received {message.message} from {sender}")
        if message.type == "step":
            personal_info = agent.storage.get("data")
            res = await generate_response(
                system=f"""
                You are are an assistant that will help a person figure out how they should be living their life: 
                {agent.storage.get('personal_info')}
                This is their daily schedule. You can suggest any deviations from it if you'd like:
                {agent.storage.get('schedule')}
                Here are a list of places next to them:
                {extract_keys(await getNearbyPlaces(personal_info['home'][0], personal_info['home'][1]), ['name', 'distance', 'price', 'rating', 'location'])}
                This is you and the person's chat history. 
                {agent.storage.get('history')}                
                """,
                user=f"""
                Where should I go at {message.message}? YOUR RESPONSE SHOULD ONLY BE IN THIS EXACT JSON FORMAT (NO PLAINTEXT):
                {{
                    "activity": str,
                    "place_name": str,
                    "latitude": float,
                    "longitude": float
                }}

                {{\n    "activity": 
                """,
                model="llama-3.2-90b-text-preview"
            )
            res_json = json.loads(res)
            agent.storage.set('coordinates', (res_json['latitude'], res_json['longitude']))
            agent.storage.get('history').append(f'{message.message}: {res}')
            await ctx.send(
                sender, 
                AgentState.parseObj(dict({'address': sender, 'coordinates': (res_json['latitude'], res_json['longitude'])}, **agent.storage.get('data')))
            )

        elif message.type == "message":
            agent.storage.get('history').append(f'Context: {message.message}')

    @agent.on_event("startup")
    async def introduce_agent(ctx: Context):
        ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")

    return agent

async def create_agents(personal_infos: list) -> list[Agent]:
    
    tasks = []

    for index, personal_info in enumerate(personal_infos):
        tasks.append(create_agent(personal_info, index + 8001))

    return await asyncio.gather(*tasks)