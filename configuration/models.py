from pydantic import BaseModel, Field


class MaliciousWords(BaseModel):
    word: str = Field(...)

    class Config:
        orm_mode = True
