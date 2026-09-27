from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "What to Eat"
    debug: bool = False

    db_type: Literal["mysql", "sqlite"] = "mysql"

    # MySQL数据库配置
    db_host: str = "192.168.1.245"
    db_port: int = 3308
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "XZY_DEMO"

    # 连接池配置
    pool_size: int = 20
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    pool_timeout: int = 30
    echo: bool = False

    # SQLite配置
    sqlite_db_path: str = "./data/what2eat.sqlite3"

    # Redis配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    auth_redis_db: int = 0
    cache_redis_db: int = 1

    @computed_field
    @property
    def database_url(self) -> str:
        if self.db_type == "mysql":
            return (
                f"mysql+aiomysql://{self.db_user}:{quote_plus(self.db_password)}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        elif self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")

    @computed_field
    @property
    def engine_options(self) -> dict:
        if self.db_type == "mysql":
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                "echo": self.echo,
            }
        return {"echo": self.echo}

    @computed_field
    @property
    def auth_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.auth_redis_db}"

    @computed_field
    @property
    def cache_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.cache_redis_db}"

    jwt_secret: str = "龘爨麤鬻籱灪蠼蠛纛齉鬲靐龗齾龕鑪鸙饢驫麣"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
