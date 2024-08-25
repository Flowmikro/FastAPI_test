from fastapi import Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


from app_settings import get_session
from bet.schemas import BetSchema
from bet.models import BetModel
from game.models import GameModel
from user.models import UserModel


async def game_is_started(
        bet: BetSchema,
        session: AsyncSession = Depends(get_session)
):
    return (
        (await session.execute(
            select(GameModel.game_over)
            .where(GameModel.id == bet.game_id))
         ).scalar_one_or_none()
    )


async def get_user_balance(
        bet: BetSchema,
        session: AsyncSession = Depends(get_session)
):
    return (
        (await session.execute(
            select(UserModel.balance)
            .where(UserModel.id == bet.user_id))
         ).scalar_one_or_none()
    )


async def update_user_balance(
        bet: BetSchema,
        session: AsyncSession = Depends(get_session)
):
    await session.execute(
        update(UserModel)
        .where(UserModel.id == bet.user_id)
        .values(
            balance=UserModel.balance - bet.bet_amount,
            frozen_balance=UserModel.frozen_balance + bet.bet_amount,
        ).execution_options(synchronize_session="fetch")
    )


async def create_bet_game(
        bet: BetSchema,
        session: AsyncSession = Depends(get_session)
):
    db_game = BetModel(**bet.model_dump())
    session.add(db_game)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A game with game such_id already exists."
        )


async def get_all_user_games(
        user_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = (
        await session.execute
        (select(BetModel).where(BetModel.user_id == user_id))
    ).scalars().all()
    return jsonable_encoder(result)
