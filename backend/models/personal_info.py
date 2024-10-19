from pydantic import BaseModel


class PersonalInfo(BaseModel):
    name: str
    home_lat: float
    home_long: float