from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app_settings import get_session
from .schemas import UserSchema, UserBalanceSchema
from .models import UserModel

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import get_session
from .schemas import UserSchema, UserBalanceSchema
from . import crud_services

router = APIRouter()


@router.post('/create-user')
async def create_user(user: UserSchema, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Создать пользователя
    """
    await crud_services.create_user(user=user, session=session)
    return JSONResponse(content={
            "status": "ok",
            "data": user.model_dump()
        },
        status_code=status.HTTP_201_CREATED,
    )


@router.get('/get-all-users')
async def get_all_users(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Вывести всех пользователей
    """
    result = await crud_services.get_all_users(session=session)
    return JSONResponse(content={
            "data": result
        },
        status_code=status.HTTP_200_OK,
    )


@router.post('/update_balance')
async def update_balance(
        balance: UserBalanceSchema,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    """
    Пополнение баланса пользователя
    """

    await crud_services.update_user_balance(balance=balance, session=session)

    return JSONResponse(content={
            "message": "Balance updated successfully"
        }, status_code=status.HTTP_200_OK
    )
