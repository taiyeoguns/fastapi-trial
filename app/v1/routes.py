import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from app.common.dependencies import check_api_key, is_valid
from app.common.schemas import UserSchema, UserResponseSchema
from app.common.types import PageNum, PerPage, Session
from app.v1.logic import create_user, get_all_users, get_user
from dataclasses import asdict

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(check_api_key)])


@router.get(
    "/users",
    summary="Users endpoint",
    description="Users endpoint description",
    responses={"200": {"model": Page[UserResponseSchema]}},
    dependencies=[Depends(is_valid)],
)
async def get_all_users_handler(
    session: Session, page: PageNum = 1, per_page: PerPage = 10
):
    logger.info("getting all users...")
    paged_data = await get_all_users(session, page, per_page)
    paged_data.items = [UserResponseSchema(**asdict(user)) for user in paged_data.items]
    return paged_data


@router.get(
    "/user/{user_id}",
    summary="User endpoint",
    description="User endpoint description",
    responses={"200": {"model": UserResponseSchema}},
    dependencies=[Depends(is_valid)],
)
async def get_user_handler(user_id, session: Session):
    logger.info("getting user...")
    user = await get_user(session, user_id)
    return UserResponseSchema(**asdict(user))


@router.post(
    "/users",
    summary="Create user endpoint",
    description="Create user endpoint description",
    responses={"201": {"model": UserResponseSchema}},
    dependencies=[Depends(is_valid)],
    status_code=HTTPStatus.CREATED,
)
async def create_user_handler(user_payload: UserSchema, session: Session):
    logger.info("creating user...")
    user = await create_user(session, user_payload)
    return UserResponseSchema(**asdict(user))
