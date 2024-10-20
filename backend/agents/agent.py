from utils.llm import generate_response
from models.personal_info import PersonalInfo
import base64
import asyncio
import uagents
from models.message import Message

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

    agent.storage.set('personal_info', personal_info)
    agent.storage.set('history', [])
    agent.storage.set('schedule', schedule)

    @agent.on_message(model=Message, replies=Message)
    async def on_message(ctx: uagents.Context, sender: str, message: Message):
        if message.type == 'update':
            res = generate_response(
                system=f"""
                You are are a person with this personal info, living their life: 
                {agent.storage.get('personal_info')}
                This is your daily schedule. You can deviate from it if you'd like:
                {agent.storage.get('schedule')}
                What are you going to do at {message}?
                """,
                user=f"""
                {agent.storage.get('history')}
                {message}: 
                """
            )
            ctx.send(res)
            agent.storage.get('history').append(f'{message}: {res}')

    return agent

async def create_agents(personal_infos: list):
    
    tasks = []

    for personal_info in personal_infos:
        tasks.append(create_agent(personal_info))

    return await asyncio.gather(*tasks)