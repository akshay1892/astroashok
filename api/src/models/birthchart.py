from pydantic import BaseModel

class BirthChart(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    timezone: str

