import pytest
from sqlalchemy import insert, select

from app.auth.models import role
from app.database import Base
from tests.conftest import client, async_session_maker, engine_test


async def test_add_role():

    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Роль не добавилась"


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string1",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string1",
        "role_id": 1
    })

    assert response.status_code == 201