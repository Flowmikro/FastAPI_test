import contextlib
from typing import AsyncIterator

from fastapi import FastAPI

import app_settings
from game.routers import router as game_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app_settings.db_manager.init(app_settings.settings.database_url)
    yield
    await app_settings.db_manager.close()


app = FastAPI(title="GameAPI", lifespan=lifespan)
app.include_router(game_router, prefix='/api/game', tags=['Game'])
