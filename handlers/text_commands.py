from pydantic import BaseModel

class Commands(BaseModel):

    my_locations: str = 'Мои локации'
    my_subscriptions: str = 'Мои подписки'
    weather_now: str = 'Погода здесь и сейчас'
    request_location: str = 'request_location'
    get_menu: str = 'get_menu'
    get_help: str = 'памагити'
    add_location: str = 'Добавить локацию'

    def get_location_weather(self, location_name) -> str:
        return f'location_weather {location_name}'

commands = Commands()
