from urllib.parse import quote_plus
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

ENV_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    DB_TYPE: Literal["MySQL", "PostgreSQL"] = "PostgreSQL"

    # MySQL数据库配置
    MYSQL_DB_HOST: str = "192.168.1.245"
    MYSQL_DB_PORT: int = 3308
    MYSQL_DB_USER: str = "root"
    MYSQL_DB_PASSWORD: str = "XZY@12345"
    MYSQL_DB_NAME: str = "XZY_DEMO"

    # PostgreSQL数据库配置
    PG_DB_HOST: str = "localhost"
    PG_DB_PORT: int = 5432
    PG_DB_USER: str = "root"
    PG_DB_PASSWORD: str = "yqb12345"
    PG_DB_NAME: str = "project"

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

    @computed_field
    @property
    def DB_URL(self) -> str:
        if self.DB_TYPE == "MySQL":
            return (
                f"mysql+aiomysql://{self.MYSQL_DB_USER}:{quote_plus(self.MYSQL_DB_PASSWORD)}"
                f"@{self.MYSQL_DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DB_NAME}"
            )
        elif self.DB_TYPE == "PostgreSQL":
            return (
                f"postgresql+asyncpg://{self.PG_DB_USER}:{quote_plus(self.PG_DB_PASSWORD)}"
                f"@{self.PG_DB_HOST}:{self.PG_DB_PORT}/{self.PG_DB_NAME}"
            )
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.DB_TYPE}")

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


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
