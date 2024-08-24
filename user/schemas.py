from decimal import Decimal

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_name: str = Field(min_length=3, max_length=15)


class UserBalanceSchema(BaseModel):
    user_id: int
    balance: Decimal = Field(ge=0.01, decimal_places=2)
