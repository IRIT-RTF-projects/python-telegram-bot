from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.crud_base import CrudBase
from models import Subscription, Location


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
        location_ids = [l.id for l in locations]
        subscriptions = await session.execute(
            select(Subscription)
            .join(Location, Location.id == Subscription.location_id)
            .where(Subscription.id.in_(location_ids))
        )
        return subscriptions.scalars().all()
    
    async def get(
            self,
            item_id: int,
            session: AsyncSession
    ):
        obj = await session.execute(
            select(Subscription)
            .join(Location, Location.id == Subscription.location_id)
            .where(Subscription.id == item_id)
        )

subscription_crud = SubscriptionCrud(Subscription)