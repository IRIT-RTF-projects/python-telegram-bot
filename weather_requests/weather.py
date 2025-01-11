import asyncio
from typing import List

from open_meteo import Forecast, OpenMeteo
from open_meteo.models import DailyParameters
from pydantic import BaseModel

from presets.day_weather import (
    get_detailed_day_report,
    get_short_day_report,
    parse_weather_now
)


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

    def parse_forecast(
            self,
            forecast: Forecast,
            number_of_days: int,
            detail_type: str
    ) -> str:
        if number_of_days < 0 or number_of_days > 14:
            raise Exception('invalid number of days must be in 1:14 range')
        forecast = forecast.to_dict()
        days = [None for _ in range(15)]
        for name, values_list in forecast['daily'].items():
            if not values_list:
                continue
            for i in range(len(values_list)):
                days[i] = days[i] or {}
                days[i][name] = values_list[i]

        result = ''
        for i in range(number_of_days):
            day = days[i]
            if not day:
                continue
            day_report = None
            if detail_type == 'detailed':
                day_report = get_detailed_day_report(day)
            if detail_type == 'short':
                day_report = get_short_day_report(day)
            result += day_report
        return result

    async def get_weather_forecast(
            self,
            latitude: float,
            longitude: float,
            number_of_days: int,
            weather_now: bool = False,
            detail_type: str = 'detailed',
    ):
        params = self.detailed_request_params
        params.latitude = latitude
        params.longitude = longitude
        forecast = await self.do_api_call(params=params)
        response = ''
        if weather_now:
            response += parse_weather_now(forecast.current_weather.to_dict()) or ''
        response += self.parse_forecast(
            forecast, number_of_days, detail_type
        ) or ''
        return response


weather = Weather()


if __name__ == '__main__':
    # test connection to open-meteo
    async def main():
        forecast: Forecast = await weather.get_weather_forecast(
            10.0, 10.0, 5, True
        )
        print(forecast)

    asyncio.run(main())
