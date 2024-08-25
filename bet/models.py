from decimal import Decimal

from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_settings import Base


class BetModel(Base):
    __tablename__ = "bet"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), unique=True)
    bet_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    win_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    game_finished: Mapped[bool] = mapped_column(default=False)

    user: Mapped["UserModel"] = relationship(
        back_populates='bet'
    )
    game: Mapped["GameModel"] = relationship(
        back_populates="bet",
        single_parent=True,
    )
