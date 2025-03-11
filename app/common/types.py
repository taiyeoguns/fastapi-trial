from typing import Annotated

from fastapi import Depends, Query, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database import get_session

Session = Annotated[AsyncSession, Depends(get_session)]

ApiKey = Annotated[str, Security(APIKeyHeader(name="X-Api-Key", auto_error=False))]

PageNum = Annotated[int, Query(ge=1)]
PerPage = Annotated[int, Query(ge=1)]
