import asyncio
import uagents.experimental
from agents.generation import generate_demographic
from agents.agent import create_agents
import uagents
from models.message import Message

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

    proto = uagents.Protocol(name="proto", version="1.0")

    master_agent = uagents.Agent(name='master')
    master_agent.include(proto)
    @master_agent.on_interval(period=1.0)
    async def on_interval(ctx: uagents.Context):
        await ctx.broadcast(proto.digest, message=Message(message=str(time)))

    bureau = uagents.Bureau(agents=agents)
    bureau.add(master_agent)
    for agent in agents:
        agent.include(proto)
        
    await bureau.run_async()

asyncio.run(main())