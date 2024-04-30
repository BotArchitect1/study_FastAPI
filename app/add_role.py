import asyncio

from app.auth.models import Role
from app.database import async_session_maker


async def seed_roles():
    async with async_session_maker() as session:
        roles = [
            Role(id=1, name="user", permissions=None),
            Role(id=2, name="admin", permissions=None)
        ]
        session.add_all(roles)
        await session.commit()

asyncio.run(seed_roles())
