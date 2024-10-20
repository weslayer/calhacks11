from utils.llm import generate_response
import asyncio
from uagents import Agent, Context
from models.message import Message
from yelp.yelp import getNearbyPlaces

def extract_keys(objects, keys):
    return [{key: obj[key] for key in keys if key in obj} for obj in objects]


async def create_agent(personal_info, port):

    agent = Agent(
        name=personal_info["name"], 
        port=port,
        endpoint=[f"http://127.0.0.1:{port}/endpoint"],
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

    agent.storage.set('personal_info', personal_info)
    agent.storage.set('history', [])
    agent.storage.set('schedule', schedule)

    @agent.on_message(model=Message, replies=Message)
    async def on_message(ctx: Context, sender: str, message: Message):
        res = await generate_response(
            system=f"""
            You are are a person with this personal info, living their life: 
            {agent.storage.get('personal_info')}
            This is your daily schedule. You can deviate from it if you'd like:
            {agent.storage.get('schedule')}
            Here are a list of places next to you:
            {extract_keys(await getNearbyPlaces(agent.storage.get('personal_info')['home'][0], agent.storage.get('personal_info')['home'][1]), ['name', 'distance', 'price', 'rating', 'location'])}
            What are you going to do at {message.message}? RESPOND IN THIS JSON FORMAT:
            {{
                "activity": str,
                "place_name": str,
                "location": {{
                    "latitude": float,
                    "longitude": float
                }}
            }}
            """,
            user=f"""
            {agent.storage.get('history')}
            {message.message}: 
            """
        )
        print(res)
        ctx.send(destination=sender, message=res)
        agent.storage.get('history').append(f'{message.message}: {res}')

    @agent.on_event("startup")
    async def introduce_agent(ctx: Context):
        ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")

    return agent

async def create_agents(personal_infos: list) -> list[Agent]:
    
    tasks = []

    for index, personal_info in enumerate(personal_infos):
        tasks.append(create_agent(personal_info, index + 8001))

    return await asyncio.gather(*tasks)