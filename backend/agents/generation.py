import sys
import os
import json
import random
import asyncio

sys.path.append(os.path.abspath('./'))

from utils.llm import generate_response

async def generate_demographic(age_groups, zipcode_income) -> list:
    '''Generates all sets of people in age_groups asynchronously'''

    async def generate_demo_set(num_people: int, age_range: str, median_income: str) -> list:
        '''Generates a set of num_people given age and income'''
        output = await generate_response(
            system=f"Generate a set of EXACTLY {str(num_people)} person(s) within the age range {age_range} in which the median income is {median_income}. Please try to be as accurate with your distribution representation as possible. Return your output as ONLY strictly JSON format. It should be a list of JSON objects with ONLY these properties: name, age, income, gender, race, occupation, hobbies, marital_status, number_of_children",
            user="[\n   {",
        )
        print(output)
        return list(json.loads(output))
    
    tasks = []
    for age_range, age_range_data in age_groups.items():
        tasks.append(generate_demo_set(age_range_data['population'], age_range, age_range_data['median_income']))
    
    # Run all tasks asynchronously
    all_demo_sets = await asyncio.gather(*tasks)

    demographic = []
    for sub_demo in all_demo_sets:
        for person in sub_demo:
            # Add persons home coordinates based on income
            zipcode = (
                        zipcode_income.get(person["income"] * random.uniform(0.75, 1.25)) or 
                        zipcode_income[min(zipcode_income.keys(), 
                        key = lambda key: abs(key-(person["income"] * random.uniform(0.75, 1.25))))]
                    )
            person["home"] = (zipcode[0] + random.uniform(-0.001, 0.001), zipcode[1] + random.uniform(-0.001, 0.001))
            demographic.append(person)

    return demographic
