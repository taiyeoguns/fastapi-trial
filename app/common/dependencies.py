import logging
from http import HTTPStatus

from fastapi import HTTPException, Request

from app.common.authentication import get_user_by_api_key
from app.common.types import ApiKey, Session

logger = logging.getLogger(__name__)


def is_valid(request: Request):
    return True


async def check_api_key(session: Session, api_key_header: ApiKey):
    if api_key_header is None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Missing API Key")

    return await get_user_by_api_key(session, api_key_header)
