AGE_DEMO_GROUPS = {
    "Under 25": {
        "population": 9,
        "median_income": "$95,000"
    },
    "25 - 44": {
        "population": 20,
        "median_income": "$195,000"
    },
    "45 - 65": {
        "population": 13,
        "median_income": "$130,000"
    },
    "Over 65": {
        "population": 8,
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

import sys
import os
import json
import random
import asyncio

sys.path.append(os.path.abspath('./'))

from utils.llm import generate_response

async def generate_demo_set(num_people: int, age_range: str, median_income: str) -> list:
    '''Generates a set of num_people given age and income'''
    raw_output = generate_response(message=f"Generate a set of {str(num_people)} people within the age range {age_range} within which the median income is {median_income}. Please try to be as accurate with your distribution representation as possible. Return your output as ONLY strictly JSON format. Do not include plaintext. Include the following properties: name, age, income, gender, race, occupation, hobbies, marital_status, number_of_children", prefill="```json\n[\n   {")
    json_string = raw_output[raw_output.index("["):raw_output.rindex("]")+1]
    return list(json.loads(json_string))

async def generate_demographic() -> list:
    '''Generates all sets of people in AGE_DEMO_GROUPS asynchronously'''
    tasks = []
    for age_range, age_range_data in AGE_DEMO_GROUPS.items():
        tasks.append(generate_demo_set(age_range_data['population'], age_range, age_range_data['median_income']))
    
    # Run all tasks asynchronously
    all_demo_sets = await asyncio.gather(*tasks)

    demographic = []
    for sub_demo in all_demo_sets:
        for person in sub_demo:
            # Add persons home coordinates based on income
            zipcode = (
                        ZIPCODES_COORDS_INCOME.get(person["income"] * random.uniform(0.75, 1.25)) or 
                        ZIPCODES_COORDS_INCOME[min(ZIPCODES_COORDS_INCOME.keys(), 
                        key = lambda key: abs(key-(person["income"] * random.uniform(0.75, 1.25))))]
                    )
            person["home"] = (zipcode[0] + random.uniform(-0.001, 0.001), zipcode[1] + random.uniform(-0.001, 0.001))
            demographic.append(person)

    return demographic

# How to run ```x = asyncio.run(generate_demographic()))```