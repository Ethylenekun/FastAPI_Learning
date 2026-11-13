from fastapi import FastAPI, Request

from app.api.v1 import router
from app.lifespan import lifespan
from app.db.database import check_db_status
from app.core.exceptions import global_exception_handler

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)

app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health", tags=["默认"])
async def check_status(request: Request):
    return {"fastapi": "OK", "db": await check_db_status(request)}
