from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, Field, SQLModel


class UserBase(SQLModel):
    name: str


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(unique=True, index=True, nullable=False, default_factory=uuid4)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=datetime.utcnow,
    )


class UserCreate(UserBase):
    """"""


class UserResponse(UserBase):
    uuid: UUID
    created_at: datetime
