import os
from urllib.parse import quote_plus
from functools import lru_cache
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, BaseModel

ENV_DIR = Path(__file__).resolve().parents[2]


class DataBaseSettings(BaseModel):
    DB_TYPE: Literal["MySQL", "PostgreSQL"] = "MySQL"

    # MySQL数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "test"
    MYSQL_PASSWORD: str = "test"
    MYSQL_DB: str = "test"

    # PostgreSQL数据库配置
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "test"
    PG_PASSWORD: str = "test"
    PG_DB: str = "test"

    # 连接池配置
    # 必选参数
    pool_size: int = 20
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_pre_ping: bool = True

    # 可选调优参数
    pool_recycle: int = 3600
    pool_use_lifo: bool = False
    echo: bool = False

    # 数据库连接
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "MySQL":
            return (
                f"mysql+aiomysql://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
                f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            )
        elif self.DB_TYPE == "PostgreSQL":
            return (
                f"postgresql+asyncpg://{self.PG_USER}:{quote_plus(self.PG_PASSWORD)}"
                f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
            )
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.DB_TYPE}")

    # 数据库引擎配置
    @computed_field
    @property
    def engine_options(self) -> dict:
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "pool_use_lifo": self.pool_use_lifo,
            "echo": self.echo,
        }


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    APP_NAME: str = "FastAPI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DB: DataBaseSettings = DataBaseSettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="_",
        env_nested_max_split=1,
        env_prefix="DEMO_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "prod")
    env_file = f".env.{env}"
    logger.info(f"正在加载配置: {env_file}")
    settings = Settings(_env_file=env_file)  # type: ignore
    logger.info(f"成功加载 {env} 环境配置 for {settings.APP_NAME}")
    return settings


settings = get_settings()

if __name__ == "__main__":
    print(settings.DB.DATABASE_URL)
