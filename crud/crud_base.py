from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CrudBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            item_id: int,
            session: AsyncSession
    ):
        obj = await session.execute(
            select(self.model).where(
                self.model.id == item_id
            )
        )
        return obj.scalars().first()

    async def get_all(
            self,
            session: AsyncSession
    ):
        objs = await session.execute(
            select(self.model)
        )
        return objs.scalars().all()

    async def create(
            self,
            obj_in: Dict[str, any],
            session: AsyncSession
    ):
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            item_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == item_id
            )
        )
        db_obj = db_obj.scalars().first()
        if not db_obj:
            return
        await session.delete(db_obj)
        await session.commit()

    async def get_first_by_attribute(
            self,
            attr_name: str,
            attr_value: any,
            session: AsyncSession
    ):
        attribute = getattr(self.model, attr_name)
        obj = await session.execute(
            select(self.model).where(
                attribute == attr_value
            )
        )
        return obj.scalars().first()

    async def get_all_by_attribute(
            self,
            attr_name: str,
            attr_value: any,
            session: AsyncSession
    ):
        attribute = getattr(self.model, attr_name)
        obj = await session.execute(
            select(self.model).where(
                attribute == attr_value
            )
        )
        return obj.scalars().all()

    async def get_by_multiple_attributes(
        self,
        attrs: Dict[str, any],
        session: AsyncSession
    ):
        equality_expressions = [
            getattr(self.model, name) == value for name, value in attrs.items()
        ]
        objects = await session.execute(
            select(self.model).where(*equality_expressions)
        )
        return objects.scalars().first()
