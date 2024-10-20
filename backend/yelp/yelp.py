import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()


async def getNearbyPlaces(lat: float, long: float, radius: int=1000):
    res = requests.get(f'https://api.yelp.com/v3/businesses/search?latitude={lat}&longitude={long}&radius={radius}',
      headers={'Authorization': f'Bearer {os.environ.get("YELP_API_KEY")}'}
    )
    res = res.json()
    return random.sample(res['businesses'], 10)