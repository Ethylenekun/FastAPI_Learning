from typing import Annotated

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from fastapi import Depends

from src.core.config import settings
from src.core.base_model import Base
from src.dishes.model import Dish

engine = create_async_engine(settings.database_url, **settings.engine_options)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with SessionFactory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功")


async def check_db_status():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        return "OK" if result.scalar_one() == 1 else "NOT OK"
