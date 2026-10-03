from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

# from src.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("应用启动，开始加载所有资源...")
    # await create_db_and_tables()

    yield

    logger.info("应用关闭，资源已释放。")
