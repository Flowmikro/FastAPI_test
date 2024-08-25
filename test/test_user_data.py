import pytest
from fastapi import HTTPException

from test.conftest import async_session_maker

from bet.schemas import BetSchema
from bet import crud_services as bet_crud_services

from user.models import UserModel
from user.schemas import UserBalanceSchema
from user import crud_services


@pytest.mark.asyncio
async def test_create_users():
    async with async_session_maker() as session:
        session.add(UserModel(user_name='test_user1'))
        session.add(UserModel(user_name='test_user2', balance=10000))
        await session.commit()


@pytest.mark.asyncio
async def test_get_all_users():
    async with async_session_maker() as session:
        result = await crud_services.get_all_users(session=session)
        assert len(result) != 3


@pytest.mark.asyncio
async def test_update_user_balance():
    async with async_session_maker() as session:
        balance_update = UserBalanceSchema(user_id=1, balance=50)
        await crud_services.update_user_balance(balance_update, session)

        updated_user = await session.get(UserModel, 1)
        assert updated_user.balance == 50


@pytest.mark.asyncio
async def test_update_nonexistent_user_balance():
    async with async_session_maker() as session:
        balance_update = UserBalanceSchema(user_id=9999, balance=50)

        with pytest.raises(HTTPException) as exc_info:
            await crud_services.update_user_balance(balance_update, session)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_update_user_balance():
    async with async_session_maker() as session:
        bet = BetSchema(user_id=2, bet_amount=20, game_id=1)
        await bet_crud_services.update_user_balance(bet, session)
        updated_user = await session.get(UserModel, 2)

        assert updated_user.balance == 9980
        assert updated_user.frozen_balance == 20
