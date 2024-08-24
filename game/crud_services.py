from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings.session_manager import get_session

from .schemas import GameSchema
from .models import GameModel


async def create_game(
        game: GameSchema,
        session: AsyncSession = Depends(get_session)
) -> None:
    """
    Создание игры
    """
    db = GameModel(**game.model_dump())
    session.add(db)
    await session.commit()


async def get_all_games(session: AsyncSession = Depends(get_session)) -> [GameModel]:
    """
    Получение всех игр
    """
    result = (await session.execute(select(GameModel))).scalars().all()
    return jsonable_encoder(result)
