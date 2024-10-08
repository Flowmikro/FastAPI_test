from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import get_session
from .schemas import UserSchema, UserBalanceSchema
from .models import UserModel


async def create_user(
        user: UserSchema,
        session: AsyncSession = Depends(get_session)
):
    db = UserModel(**user.model_dump())
    session.add(db)
    await session.commit()


async def get_all_users(session: AsyncSession = Depends(get_session)):
    result = (await session.execute(select(UserModel))).scalars().all()
    return jsonable_encoder(result)


async def update_user_balance(
        balance: UserBalanceSchema,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        update(UserModel).where(UserModel.id == balance.user_id).values(
            balance=UserModel.balance + balance.balance
        )
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    await session.commit()