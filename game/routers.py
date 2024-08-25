from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import get_session
from .enum_choices import GameResultUpdateEnum, GameEnum
from .schemas import GameSchema
from . import crud_services

router = APIRouter()


@router.post('/create-game')
async def create_game(
        game: GameSchema,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
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
async def get_games(
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    """
    Выводит все игры
    """
    result = await crud_services.get_all_games(session=session)
    return JSONResponse(content={
        "data": result
    },
        status_code=status.HTTP_200_OK
    )


@router.put('/update_game/{event_id}')
async def update_games(
        event_id: int,
        game_status: GameResultUpdateEnum,
        session: AsyncSession = Depends(get_session)
):
    """
    Update game status
    """
    # Преобразуем статус из GameResult в BetResult
    if game_status == GameResultUpdateEnum.LOSE:
        game_result = GameEnum.LOSE
    elif game_status == GameResultUpdateEnum.WIN:
        game_result = GameEnum.WIN
    else:
        raise HTTPException(detail={'Invalid game_status'}, status_code=status.HTTP_404_NOT_FOUND)
    game_is_finished = await crud_services.game_is_finished(event_id=event_id, session=session)

    # Если игра закончилась
    if game_is_finished:
        return JSONResponse(content={
            "message": "Game is already finished"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    await crud_services.update_game_status(
        event_id=event_id,
        game_result=game_result,
        session=session,
    )

    await crud_services.finalize_game_bets(
        game_id=event_id,
        game_status=game_result,
        session=session,
    )
    return JSONResponse(content={
        "message": "Game status updated successfully"
    }, status_code=status.HTTP_200_OK
    )
