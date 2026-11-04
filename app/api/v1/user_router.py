from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=["用户管理"])


@user_router.get("/")
async def root():
    return {"postion": "user"}
