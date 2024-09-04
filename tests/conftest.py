import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.async_session import get_async_session

from app.main import app

import os
from dotenv import load_dotenv

from sqlalchemy.pool import NullPool

from app.models.shop_models import metadata

load_dotenv()

DATABASE_URL_TEST = os.getenv('TEST_DB_URL')

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session():
    async with async_session_maker() as async_session:
        yield async_session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="function")
def engine():
    get_engine = create_async_engine(
        os.getenv('TEST_DB_URL')
    )
    yield get_engine
    get_engine.sync_engine.dispose()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as get_client:
        yield get_client


@pytest.fixture(scope="function")
async def session(engine):
    async with AsyncSession(engine) as get_session:
        yield get_session
