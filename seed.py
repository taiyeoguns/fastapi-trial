import asyncio
from uuid import uuid4

from decouple import config

from app.common.authentication import get_user_by_api_key
from app.common.database import SessionLocal
from app.common.factories import UserFactory


async def seed_users():
    async with SessionLocal() as session:
        existing_admin_user = await get_user_by_api_key(
            session, config("ADMIN_TOKEN"), raise_exception=False
        )
        if not existing_admin_user:
            await session.run_sync(
                UserFactory.create_instance,
                first_name="Admin",
                last_name="User",
                api_key=config("ADMIN_TOKEN", uuid4().hex),
            )
        await session.run_sync(UserFactory.create_instances, 10)


if __name__ == "__main__":
    asyncio.run(seed_users())
