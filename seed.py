import asyncio
from uuid import uuid4

from decouple import config
from sqlalchemy import select

from app.common.database import SessionLocal
from app.common.factories import UserFactory
from app.common.models import User


async def seed_users():
    query = select(User).where(User.api_key == config("ADMIN_TOKEN"))
    async with SessionLocal() as session:
        user_result = await session.execute(query)
        existing_admin_user = user_result.scalar_one_or_none()
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
