import pytest

from test.conftest import async_session_maker

from game.enum_choices import GameEnum
from game.models import GameModel
from game import crud_services


@pytest.mark.asyncio
async def test_create_games():
    async with async_session_maker() as session:
        session.add(GameModel(first_player='first_test1', second_player='second_test1'))
        session.add(GameModel(first_player='first_test2', second_player='second_test2'))
        await session.commit()


@pytest.mark.asyncio
async def test_get_all_games():
    async with async_session_maker() as session:
        result = await crud_services.get_all_games(session=session)
        assert len(result) != 3


@pytest.mark.asyncio
async def test_get_all_games():
    async with async_session_maker() as session:
        result = await crud_services.get_all_games(session=session)
        assert len(result) != 3


@pytest.mark.asyncio
async def test_game_is_finished():
    async with async_session_maker() as session:
        result = await crud_services.game_is_finished(event_id=1, session=session)
        assert result is False


@pytest.mark.asyncio
async def test_update_game_status():
    async with async_session_maker() as session:
        await crud_services.update_game_status(event_id=1, game_result=GameEnum.WIN, session=session)

        updated_game = await session.get(GameModel, 1)
        assert updated_game.game_over is True
        assert updated_game.first_player_result == GameEnum.WIN
