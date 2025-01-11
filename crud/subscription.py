from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.crud_base import CrudBase
from models import Location, Subscription


class SubscriptionCrud(CrudBase):

    async def get_user_subscriptions(
            self,
            user_id: int,
            session: AsyncSession
    ):
        locations = await session.execute(
            select(Location)
            .where(Location.user_id == user_id)
        )
        locations = locations.scalars().all()
        location_ids = [location.id for location in locations]
        subscriptions = await session.execute(
            select(Subscription, Location)
            .join(Location)
            .where(Subscription.location_id.in_(location_ids))
            .options(selectinload(Subscription.location))
        )
        subscriptions = subscriptions.scalars().all()
        return subscriptions

    async def get(
            self,
            item_id: int,
            session: AsyncSession
    ):
        obj = await session.execute(
            select(Subscription, Location)
            .join(Location)
            .where(Subscription.id == item_id)
            .options(selectinload(Subscription.location))
        )
        return obj.scalars().first()

    async def get_all(
            self,
            session: AsyncSession
    ):
        subscriptions = await session.execute(
            select(Subscription)
            .options(
                selectinload(Subscription.location)
                .selectinload(Location.user)
            )
        )
        subscriptions = subscriptions.scalars().all()
        return subscriptions


subscription_crud = SubscriptionCrud(Subscription)
