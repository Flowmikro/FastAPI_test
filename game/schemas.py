from pydantic import BaseModel, Field


class GameSchema(BaseModel):
    first_player: str = Field(min_length=3, max_length=15)
    second_player: str = Field(min_length=3, max_length=15)
