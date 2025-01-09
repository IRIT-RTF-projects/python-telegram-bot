from typing import List, Tuple

from pydantic import BaseModel

class Commands(BaseModel):

    my_locations: str = 'Мои локации'
    my_subscriptions: str = 'Мои подписки'
    weather_now: str = 'Погода здесь и сейчас'
    request_location: str = 'request_location'
    get_menu: str = 'get_menu'
    get_help: str = 'Помощь'
    add_location: str = 'Добавить локацию'
    add_subscription: str = 'Добавить подписку'

    def get_subscription_location(self, location_name) -> str:
        return f'subscrlctn {location_name}'

    def get_location_weather(self, location_name) -> str:
        return f'location_weather {location_name}'
    
    detail_types: List[Tuple[str, str]] = [('Детализированный отчет', 'detailed'), ('Краткий отчет', 'short')]

    def get_detail_type(self, detail_type): # detailed / short
        return f'detail_type {detail_type}'

    def get_subscription_info(self, subscription_id):
        return f'subscr_info {subscription_id}'
    
    def delete_subscription(self, subscription_id):
        return f'del_subscr {subscription_id}'


commands = Commands()
