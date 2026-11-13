from typing import cast, Annotated

from fastapi import Request, Depends
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from app.core.config import settings
from app.models.base import Base


async def setup_database_connection() -> (
    tuple[AsyncEngine, async_sessionmaker[AsyncSession]]
):
    engine: AsyncEngine = create_async_engine(
        url=settings.DB.DATABASE_URL,
        **settings.DB.engine_options,
    )

    AsyncSessionFactory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    logger.info("数据库对象已创建")

    return engine, AsyncSessionFactory


async def close_database_connection(engine: AsyncEngine) -> None:
    await engine.dispose()

    logger.info("数据库对象已销毁")


async def get_db(request: Request):
    AsyncSessionFactory = cast(
        async_sessionmaker[AsyncSession], request.state.AsyncSessionFactory
    )

    async with AsyncSessionFactory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def check_db_status(request: Request):
    engine = cast(AsyncEngine, request.state.engine)

    async with engine.begin() as conn:
        stmt = text("SELECT 1")
        result = await conn.execute(stmt)
        return "DB OK" if result.scalar_one() == 1 else "DB NOT OK"


async def create_db_and_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库及数据表已创建")
