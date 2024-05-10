from pydantic import BaseModel

class GeneralModel(BaseModel):
    type: str
    properties: dict