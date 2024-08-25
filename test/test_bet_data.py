import pytest

from test.conftest import async_session_maker

from game.models import GameModel

from bet.models import BetModel
from bet import crud_services
from bet.schemas import BetSchema


@pytest.mark.asyncio
async def test_create_best():
    async with async_session_maker() as session:
        session.add(BetModel(user_id=1, game_id=1, bet_amount=0.2))
        session.add(BetModel(user_id=2, game_id=2, bet_amount=0.2))
        await session.commit()


@pytest.mark.asyncio
async def test_game_is_started_not_finished():
    async with async_session_maker() as session:
        # Создаем игру, которая не завершена
        game = GameModel(first_player='first_test', second_player='second_test', game_over=False)
        session.add(game)
        await session.commit()

        # Создаем ставку
        bet = BetSchema(game_id=game.id, user_id=1, bet_amount=0.1)

        # Проверяем, что игра не завершена
        result = await crud_services.game_is_started(bet=bet, session=session)
        assert result is False


@pytest.mark.asyncio
async def test_game_is_started_finished():
    async with async_session_maker() as session:
        # Создаем игру, которая завершена
        game = GameModel(first_player='first_test', second_player='second_test', game_over=True)
        session.add(game)
        await session.commit()

        # Создаем ставку
        bet = BetSchema(game_id=game.id, user_id=1, bet_amount=0.1)

        # Проверяем, что игра завершена
        result = await crud_services.game_is_started(bet=bet, session=session)
        assert result is True


@pytest.mark.asyncio
async def test_get_user_balance():
    async with async_session_maker() as session:
        bet = BetSchema(user_id=7, game_id=1, bet_amount=0.1)
        balance = await crud_services.get_user_balance(bet, session)
        assert balance is None


@pytest.mark.asyncio
async def test_get_all_user_games():
    async with async_session_maker() as session:
        balance = await crud_services.get_all_user_games(user_id=1, session=session)
        assert len(balance) == 1
