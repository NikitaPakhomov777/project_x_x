from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from dotenv import load_dotenv
import os
from app.models.shop_models import Model

load_dotenv()

DB_URL = os.getenv('DB_URL')

async_engine: AsyncEngine = create_async_engine(DB_URL)

SessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with SessionLocal() as async_session:
        yield async_session


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
