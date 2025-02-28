import asyncio
from uuid import uuid4

from decouple import config

from app.common.database import SessionLocal
from app.common.factories import UserFactory


async def seed_users():
    async with SessionLocal() as session:
        await session.run_sync(
            user_factory,
            first_name="Admin",
            last_name="User",
            api_key=config("ADMIN_TOKEN", uuid4().hex),
        )
        await session.run_sync(user_factory, 10)


def user_factory(session, size=1, **kwargs):
    UserFactory._meta.sqlalchemy_session = session
    return UserFactory.create_batch(size=size, **kwargs)


if __name__ == "__main__":
    asyncio.run(seed_users())
