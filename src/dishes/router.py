from typing import Literal, Annotated

from fastapi import APIRouter, Path, Query, status, Depends
from loguru import logger

from src.core.database import SessionDep
from src.dishes.service import DishService
from src.dishes.repository import DishRepository
from src.dishes.schema import DishResponse, DishCreate, DishUpdate

router = APIRouter(prefix="/dishes", tags=["dishes"])


async def get_dish_service(session: SessionDep) -> DishService:
    repository = DishRepository(session)
    return DishService(repository)


ServiceDep = Annotated[DishService, Depends(get_dish_service)]


@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish_data: DishCreate,
    service: ServiceDep,
):
    new_dish = await service.create_dish(dish_data)
    return new_dish


@router.get("/{dish_id}", response_model=DishResponse)
async def get_dish(
    dish_id: Annotated[int, Path(..., description="菜品ID")], service: ServiceDep
):
    logger.debug(f"正在获取菜品 ID: {dish_id}")
    try:
        dish = await service.get_dish_by_id(dish_id)
        logger.info(f"获取到菜品，ID: {dish_id}")
        return dish
    except Exception as e:
        logger.error(f"获取 ID 为 {dish_id}的菜品时出错：{str(e)}")
        raise


@router.get("/", response_model=list[DishResponse])
async def list_dishes(
    service: ServiceDep,
    search: Annotated[str | None, Query(description="搜索关键词")] = None,
    order_by: Annotated[
        Literal["id", "name", "created_at"], Query(description="排序字段")
    ] = "id",
    direction: Annotated[Literal["asc", "desc"], Query(description="排序方向")] = "asc",
    limit: Annotated[int, Query(ge=1, le=500)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    dishes = await service.list_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )
    return dishes


@router.patch("/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish_data: DishUpdate,
    dish_id: Annotated[int, Path(..., description="菜品ID")],
    service: ServiceDep,
):
    dish = await service.update_dish(dish_id, dish_data)
    return dish


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    dish_id: Annotated[int, Path(..., description="菜品ID")], service: ServiceDep
):

    await service.delete_dish(dish_id)
