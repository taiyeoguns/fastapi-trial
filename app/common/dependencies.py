from http import HTTPStatus
import logging
from fastapi import HTTPException, Request

from app.common.models import User
from app.common.types import ApiKey, Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def is_valid(request: Request):
    return True


async def check_api_key(session: Session, api_key_header: ApiKey):
    if api_key_header is None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Missing API Key")

    return await get_user_by_api_key(session, api_key_header)


async def get_user_by_api_key(session, api_key):
    query = select(User).where(User.api_key == api_key)

    try:
        user_result = await session.execute(query)
    except SQLAlchemyError as exc:
        if isinstance(exc.orig, ValueError):
            raise ValueError("Invalid api key provided") from exc
        logger.exception("%s", exc)
        raise

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(HTTPStatus.FORBIDDEN, f"User with '{api_key}' not found")

    return user
