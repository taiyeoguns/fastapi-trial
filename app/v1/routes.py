import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.common.models import UserCreate, UserResponse
from app.v1.logic import create_user, get_all_users, get_user

logger = logging.getLogger(__name__)

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get(
    "/users",
    summary="Users endpoint",
    description="Users endpoint description",
    responses={"200": {"model": list[UserResponse]}},
    dependencies=[Depends(is_valid)],
)
async def get_all_users_handler(session: Session):
    logger.info("getting all users...")
    users = await get_all_users(session)
    return [UserResponse(**user.dict()) for user in users]


@router.get(
    "/user/{user_id}",
    summary="User endpoint",
    description="User endpoint description",
    responses={"200": {"model": UserResponse}},
    dependencies=[Depends(is_valid)],
)
async def get_user_handler(user_id, session: Session):
    logger.info("getting user...")
    user = await get_user(session, user_id)
    return UserResponse(**user.dict())


@router.post(
    "/users",
    summary="Create user endpoint",
    description="Create user endpoint description",
    responses={"201": {"model": UserResponse}},
    dependencies=[Depends(is_valid)],
    status_code=HTTPStatus.CREATED,
)
async def create_user_handler(user_payload: UserCreate, session: Session):
    logger.info("creating user...")
    user = await create_user(session, user_payload)
    return UserResponse(**user.dict())
