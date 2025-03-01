from typing import Annotated

from fastapi import Depends, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database import get_session

Session = Annotated[AsyncSession, Depends(get_session)]

ApiKey = Annotated[str, Security(APIKeyHeader(name="X-Api-Key", auto_error=False))]
