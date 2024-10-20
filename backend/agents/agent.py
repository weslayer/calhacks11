from utils.llm import generate_response
from models.personal_info import PersonalInfo
import base64
import asyncio
import uagents

async def create_agent(personal_info):

    agent = uagents.Agent(name=personal_info["name"], seed=personal_info["name"])

    schedule = await generate_response(
        system=f'''
        Generate a daily schedule for a person with these character traits: {str(personal_info)}. 
        Please try to represent each person as best as possible, taking into account every metric. Return your output as in ONLY strictly JSON format. Do not include plaintext.
        Here is an example schema:
            {
                "7 am - 8 am": {
                    "activity": "getting ready",
                    "location": "home"
                },
                "8 am - 12 pm": {
                    "activity": "working",
                    "location": "work"
                },
                "12 pm - 1 pm": {
                    "activity": "eating",
                    "location": "restaurant"
                },
                "1 pm - 5 pm": {
                    "activity": "working",
                    "location": "work"
                },
                "5 pm - 7 pm": {
                    "activity": "eating",
                    "location": "restaurant"
                },
                "7 pm - 10 pm": {
                    "activity": "resting",
                    "location": "home"
                },
            }
        '''
    )

    agent.storage.set('history', [])
    agent.storage.set('schedule', schedule)

    return agent

async def create_agents(personal_infos: list):
    
    tasks = []

    for personal_info in personal_infos:
        tasks.append(create_agent(personal_info))

    return await asyncio.gather(*tasks)