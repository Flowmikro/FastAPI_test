from decimal import Decimal

from pydantic import BaseModel, Field


class BetSchema(BaseModel):
    game_id: int
    user_id: int
    bet_amount: Decimal = Field(ge=0.01, decimal_places=2)
