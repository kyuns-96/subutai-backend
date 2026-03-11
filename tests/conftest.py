import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import get_db
from app.main import app
from app.models import Base

TEST_DATABASE_URL = os.getenv(
    "SUBUTAI_TEST_DATABASE_URL",
    "mysql+asyncmy://root:rootpassword@localhost:3306/subutai_test?charset=utf8mb4",
)

engine = create_async_engine(TEST_DATABASE_URL, pool_recycle=1800, pool_pre_ping=True)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def _admin_database_url(database_url: str) -> str:
    return (
        make_url(database_url).set(database=None).render_as_string(hide_password=False)
    )


async def ensure_test_database() -> None:
    database_name = make_url(TEST_DATABASE_URL).database
    admin_engine = create_async_engine(
        _admin_database_url(TEST_DATABASE_URL),
        isolation_level="AUTOCOMMIT",
        pool_recycle=1800,
        pool_pre_ping=True,
    )

    try:
        async with admin_engine.connect() as conn:
            await conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4"
                )
            )
    finally:
        await admin_engine.dispose()


@pytest.fixture(autouse=True)
async def setup_db():
    await ensure_test_database()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with TestSession() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
