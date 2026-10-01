from typing import Mapping, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, update, delete
from sqlalchemy.exc import IntegrityError

from src.dishes.model import Dish


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, dish_data: Mapping[str, Any]) -> Dish:
        dish = Dish(**dish_data)
        self.session.add(dish)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(dish)
        return dish

    async def get_by_id(self, dish_id: int) -> Dish | None:
        dish = await self.session.get(Dish, dish_id)
        return dish

    async def get_all(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[Dish]:
        stmt = select(Dish)

        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(Dish.name.ilike(pattern), Dish.description.ilike(pattern))
            )

        allowed_sort = {"id", "name", "created_at"}
        if order_by not in allowed_sort:
            order_by = "id"
        order_column = getattr(Dish, order_by, Dish.id)
        stmt = stmt.order_by(
            order_column.desc() if direction == "desc" else order_column.asc(),
        )

        limit = min(limit, 500)
        offset = max(offset, 0)
        paginated_stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(paginated_stmt)
        items = list(result.scalars().all())
        return items

    async def update(self, dish_data: Mapping[str, Any], dish_id: int) -> Dish | None:
        stmt = update(Dish).where(Dish.id == dish_id).values(**dish_data)
        await self.session.execute(stmt)
        await self.session.commit()
        dish = await self.session.get(Dish, dish_id)
        return dish

    async def delete(self, dish_id: int) -> bool:
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            return False
        stmt = delete(Dish).where(Dish.id == dish_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
