from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.common.database import BaseDbModel


class User(BaseDbModel, kw_only=True):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))
    api_key: Mapped[UUID] = mapped_column(
        UUIDType(),
        unique=True,
        index=True,
        nullable=False,
        default_factory=uuid4,
        repr=False,
    )
