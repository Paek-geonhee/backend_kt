from pydantic import BaseModel

class AnimalPost(BaseModel):
    type: str
    value: str