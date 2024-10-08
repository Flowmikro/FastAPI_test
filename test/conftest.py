import pytest
from typing import AsyncGenerator
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app_settings import get_session, Base
from main import app

# DATABASE тестовая бд
DATABASE_URL_TEST = "sqlite+aiosqlite:///./test_app.db"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция для переопределения получения асинхронной сессии в тестовом режиме
    """
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """
    Фикстура для подготовки базы данных перед запуском тестов.
    Создает таблицы перед выполнением тестов и удаляет их после завершения
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура для создания асинхронного HTTP-клиента для тестирования.
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
