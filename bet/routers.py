from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from app_settings import get_session
from .schemas import BetSchema
from . import crud_services

router = APIRouter()


@router.post('/get')
async def bet_game(
        bet: BetSchema,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    game_is_started = await crud_services.game_is_started(bet=bet, session=session)

    if game_is_started:
        return JSONResponse(content={
            "status": "error",
            "message": "Game already started"
        })

    user_balance = await crud_services.get_user_balance(bet=bet, session=session)

    if user_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_balance < bet.bet_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
        )

    # Обновление баланса пользователя
    await crud_services.update_user_balance(bet=bet, session=session)

    # Создание новой записи в таблице игр
    await crud_services.create_bet_game(bet=bet, session=session)

    return JSONResponse(content={
        "status": "ok",
    }, status_code=status.HTTP_201_CREATED)


@router.get('/get-all-user-games/{user_id}')
async def get_all_user_games(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    result = await crud_services.get_all_user_games(user_id=user_id, session=session)
    return JSONResponse(content={
        "data": result
    },
        status_code=status.HTTP_200_OK,
    )
