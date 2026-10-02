from sqlalchemy.exc import IntegrityError

from src.dishes.repository import DishRepository
from src.core.exception import NotFoundException, AlreadyExistsException
from src.dishes.schema import DishCreate, DishUpdate, DishResponse


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository

    async def create_dish(self, dish_data: DishCreate) -> DishResponse:
        data = dish_data.model_dump()
        try:
            dish = await self.repository.create(data)
            return DishResponse.model_validate(dish)
        except IntegrityError as e:
            raise AlreadyExistsException("Dish with this name already exists") from e

    async def get_dish_by_id(self, dish_id: int) -> DishResponse:
        dish = await self.repository.get_by_id(dish_id)
        if not dish:
            raise NotFoundException(f"Dish with id {dish_id} not found")
        return DishResponse.model_validate(dish)

    async def list_dishes(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[DishResponse]:
        dishes = await self.repository.get_all(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [DishResponse.model_validate(dish) for dish in dishes]

    async def update_dish(self, dish_id: int, dish_data: DishUpdate) -> DishResponse:
        try:
            update_data = dish_data.model_dump(exclude_unset=True, exclude_none=True)
            updated = await self.repository.update(update_data, dish_id)
            if not updated:
                raise NotFoundException(f"Dish with id {dish_id} not found")
            return DishResponse.model_validate(updated)
        except IntegrityError as e:
            raise AlreadyExistsException("Dish with this name already exists") from e

    async def delete_dish(self, dish_id: int) -> None:
        deleted = await self.repository.delete(dish_id)
        if not deleted:
            raise NotFoundException(f"Dish with id {dish_id} not found")
