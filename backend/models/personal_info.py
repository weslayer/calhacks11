from pydantic import BaseModel

class PersonalInfo(BaseModel):
    name: str
    home_lat: float
    home_long: float
    age: 75
    income: 1000000
    gender: str
    race: str
    occupation: str
    hobby: str
    marital_status: str
    number_of_children: int
    home: tuple[float, float]