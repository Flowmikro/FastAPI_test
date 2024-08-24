from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import get_session
from .schemas import GameSchema
from . import crud_services

router = APIRouter()


@router.post('/create-game')
async def create_game(game: GameSchema, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Создание игры
    """
    await crud_services.create_game(game=game, session=session)
    return JSONResponse(content={
        "status": "ok",
        "data": game.model_dump()
    },
        status_code=status.HTTP_201_CREATED,
    )


@router.get('/get-games')
async def get_games(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Выводит все игры
    """
    result = await crud_services.get_all_games(session=session)
    return JSONResponse(content={
        "data": result
        },
        status_code=status.HTTP_200_OK
    )

