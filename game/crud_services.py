from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings.session_manager import get_session
from bet.models import BetModel
from user.models import UserModel
from .enum_choices import GameEnum
from .schemas import GameSchema
from .models import GameModel


async def create_game(
        game: GameSchema,
        session: AsyncSession = Depends(get_session)
):
    db = GameModel(**game.model_dump())
    session.add(db)
    await session.commit()


async def get_all_games(session: AsyncSession = Depends(get_session)):
    result = (await session.execute(select(GameModel))).scalars().all()
    return jsonable_encoder(result)


async def game_is_finished(
        event_id: int,
        session: AsyncSession = Depends(get_session),
):
    return (await session.execute(select(GameModel.game_over).where(GameModel.id == event_id))).scalar_one_or_none()


async def update_game_status(
        event_id: int,
        game_result: GameEnum,
        session: AsyncSession = Depends(get_session),
):
    await session.execute(
        update(GameModel)
        .where(GameModel.id == event_id)
        .values(
            first_player_result=game_result,
            game_over=True,
        )
    )


async def finalize_game_bets(
        game_id: int,
        game_status: GameEnum,
        session: AsyncSession = Depends(get_session),
):
    # Получаем все ставки для указанной игры
    bets = await session.execute(
        select(BetModel)
        .where(BetModel.game_id == game_id, BetModel.game_finished == False)
    )
    bet_records = bets.scalars().all()
    # Обрабатываем каждую ставку
    for bet in bet_records:
        # Обновляем баланс и выигрыш
        user = await session.execute(select(UserModel).where(UserModel.id == bet.user_id))
        user_record = user.scalar_one()
        if game_status == game_status.WIN:

            # Обновляем баланс пользователя
            bet.win_amount += bet.bet_amount * 2  # Победный коэффициент
            user_record.balance += bet.bet_amount * 2  # Победный коэффициент

        bet.game_finished = True
        user_record.frozen_balance -= bet.bet_amount
        session.add(user_record)

    await session.commit()
