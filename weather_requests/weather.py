import asyncio
from typing import List, Dict
from pydantic import BaseModel

from open_meteo import OpenMeteo, Forecast
from open_meteo.models import DailyParameters

class Weather:

    class RequestParams(BaseModel):
        latitude: float
        longitude: float
        current_weather: bool
        timezone: str
        daily: List[str]

    detailed_request_params: RequestParams = RequestParams(
        latitude=0,
        longitude=0,
        current_weather=True,
        timezone='Europe/Moscow',
        daily=[
            DailyParameters.APPARENT_TEMPERATURE_MAX,
            DailyParameters.APPARENT_TEMPERATURE_MIN,
            DailyParameters.PRECIPITATION_SUM,
            DailyParameters.PRECIPITATION_HOURS,
            DailyParameters.SHORTWAVE_RADIATION_SUM,
            DailyParameters.SUNRISE,
            DailyParameters.SUNSET,
            DailyParameters.WIND_SPEED_10M_MAX,
            DailyParameters.WIND_GUSTS_10M_MAX,
            DailyParameters.WIND_DIRECTION_10M_DOMINANT,
            DailyParameters.TEMPERATURE_2M_MAX,
            DailyParameters.TEMPERATURE_2M_MIN,
        ]
    )

    async def do_api_call(self, params: RequestParams) -> Forecast:
        forecast = None
        async with OpenMeteo() as open_meteo:
            forecast = await open_meteo.forecast(**params.model_dump())
        return forecast
    
    async def parse_weather_now(self):
        pass

    async def parse_forecast(self):
        pass

    async def get_weather_forecast(
            self,
            latitude: float,
            longitude: float,
            number_of_days: int,
            weather_now: bool = False
            ):
        params = self.detailed_request_params
        params.latitude = latitude
        params.longitude = longitude
        forecast = await self.do_api_call(params=params)
        forecast_dict = forecast.to_dict()
        days = [None for _ in range(14)]
        for name, values_list in forecast_dict['daily'].items():
            if not values_list: continue
            for i in range(len(values_list)):
                days[i] = days[i] or {}
                days[i][name] = values_list[i]

        for day in days:
            if day: print(day) 
        
        return ""



weather = Weather()


if __name__ == '__main__':
    # test connection to open-meteo
    async def main():
        forecast: Forecast = await weather.get_weather_forecast(10.0, 10.0, 10, True)
        print(forecast.current_weather)

    asyncio.run(main())


