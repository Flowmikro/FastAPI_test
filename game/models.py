from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_settings import Base
from .enum_choices import GameEnum


class GameModel(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    first_player: Mapped[str]
    second_player: Mapped[str]
    first_player_result: Mapped[GameEnum] = mapped_column(default=GameEnum.NOT)
    game_over: Mapped[bool] = mapped_column(default=False)
