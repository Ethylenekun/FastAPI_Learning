from fastapi import FastAPI, Request

from app.api.v1 import router
from app.lifespan import lifespan
from app.db.database import check_db_status

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)


@app.get("/health", tags=["默认"])
async def check_status(request: Request):
    return {"fastapi": "OK", "db": await check_db_status(request)}
