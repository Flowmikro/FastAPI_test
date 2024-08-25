from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL

from app_settings import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    frozen_balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    bet: Mapped[list["BetModel"]] = relationship(
        back_populates='user',
    )