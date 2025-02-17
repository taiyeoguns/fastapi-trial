from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserResponseSchema(UserSchema):
    uuid: UUID = Field(..., serialization_alias="id")
    created_at: datetime
    updated_at: datetime
