import requests

async def getNearbyPlaces(lat: float, long: float, radius: int=1000):
    res = requests.get(f'https://api.yelp.com/v3/businesses/search?latitude={lat}&longitude={long}&radius={radius}')
    return res.json()