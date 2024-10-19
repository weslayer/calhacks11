from utils.llm import generate_response
from models.personal_info import PersonalInfo
import base64
import asyncio
import uagents

async def create_agent(personal_info: PersonalInfo):

    agent = uagents.Agent(name=personal_info.name, seed=base64.b64encode(personal_info))

    schedule = generate_response(
        system=f'''
        Generate a daily schedule for a person with these character traits: {personal_info}. 
        Please try to represent each person as best as possible, taking into account every metric. Return your output as in ONLY strictly JSON format. Do not include plaintext.
        Here is an example schema:
            {{
                "Wake Up": 8 am - 9 am,
                "Go To Work": 9 am - 12 pm,
                "Head out for Lunch": 12 pm - 1 pm,
                "Go To Work": 1 pm - 5 pm,
                "Go To Bar": 5 pm - 9 pm,
                "Go Home": 9 pm,
                "Sleep": 11 pm
            }}
        ''',
    )

    agent.storage.set('history', [])
    agent.storage.set('schedule', schedule)

    return agent

async def create_agents(personal_infos: list[PersonalInfo]):
    
    tasks = []

    for personal_info in personal_infos:
        tasks.append(create_agents(personal_info))

    return await asyncio.gather(*tasks)