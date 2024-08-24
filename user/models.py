from sqlalchemy.orm import Mapped, mapped_column

from app_settings import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=0)
    frozen_balance: Mapped[int] = mapped_column(default=0)
