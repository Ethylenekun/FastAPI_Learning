from contextlib import asynccontextmanager
from typing import TypedDict

from loguru import logger
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.db.database import (
    setup_database_connection,
    close_database_connection,
    create_db_and_tables,
)


class AppState(TypedDict):
    engine: AsyncEngine
    AsyncSessionFactory: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(_: FastAPI):
    engine, AsyncSessionFactory = await setup_database_connection()

    await create_db_and_tables(engine)

    logger.info("fastapi服务启动")

    yield AppState(engine=engine, AsyncSessionFactory=AsyncSessionFactory)

    await close_database_connection(engine=engine)

    logger.info("fastapi服务关闭")
