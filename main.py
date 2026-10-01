from typing import Annotated

from fastapi import FastAPI, status, Depends

from src.core.config import Settings, get_settings
from src.core.database import check_db_status

app = FastAPI()


# 测试端点
@app.get("/")
async def read_root(
    settings: Annotated[Settings, Depends(get_settings)],
    db_status: Annotated[int, Depends(check_db_status)],
):
    return {
        "message": f"Hello from the {settings.app_name}",
        "database_url": settings.database_url,
        "jwt_secret": settings.jwt_secret,
        "db_status": db_status,
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}
