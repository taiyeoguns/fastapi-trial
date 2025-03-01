import logging
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.common.models import User

logger = logging.getLogger(__name__)


async def get_user_by_api_key(session, api_key, raise_exception=True):
    query = select(User).where(User.api_key == api_key)

    try:
        user_result = await session.execute(query)
    except SQLAlchemyError as exc:
        if isinstance(exc.orig, ValueError):
            raise ValueError("Invalid api key provided") from exc
        logger.exception("%s", exc)
        raise

    user = user_result.scalar_one_or_none()

    if user is None and raise_exception:
        raise HTTPException(HTTPStatus.FORBIDDEN, f"User with '{api_key}' not found")

    return user
