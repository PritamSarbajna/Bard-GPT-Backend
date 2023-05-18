from pydantic import BaseModel


class BardModel(BaseModel):
    question: str