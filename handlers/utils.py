from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from crud import *
from models import Location
from models.errors import ObjectNotFoundError


async def get_user_by_id(user_id: int, session: AsyncSession):
    user = await user_crud.get(user_id, session)
    return user

async def register_user(user_id: int, chat_id: int, session: AsyncSession):
    user_data = {
        "id": user_id,
        "chat_id": chat_id
    }
    created_user = await user_crud.create(user_data, session)
    return created_user

async def get_user_locations(user_id: int, session: AsyncSession):
    locations = await location_crud.get_all_by_attribute('user_id', user_id, session)
    return locations

async def create_location(location_data: Dict[str, any], session: AsyncSession) -> Location:
    location = await location_crud.create(location_data, session)
    return location

async def check_location_exists(user_id: int, location_name: str, session: AsyncSession):
    return await location_crud.get_by_multiple_attributes({ "user_id": user_id, "name": location_name }, session)

async def create_subscription(subscription_data: Dict[str, any], session: AsyncSession):
    return await subscription_crud.create(subscription_data, session)

async def get_user_subscriptions(user_id: int, session: AsyncSession):
    return await subscription_crud.get_user_subscriptions(user_id, session)

async def get_subscription_by_id(subscription_id: int, session: AsyncSession):
    return await subscription_crud.get(subscription_id, session)

async def delete_location(location_id: int, session: AsyncSession):
    location = await location_crud.get(location_id, session)
    if not location:
        raise ObjectNotFoundError('location not found')
    await location_crud.remove(location_id, session)

async def delete_subscription(subscription_id: int, session: AsyncSession):
    subscription= await subscription_crud.get(subscription_id, session)
    if not subscription:
        raise ObjectNotFoundError('subscription not found')
    await subscription_crud.remove(subscription_id, session)