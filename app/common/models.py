from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database import BaseDbModel


class User(BaseDbModel, kw_only=True):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))
