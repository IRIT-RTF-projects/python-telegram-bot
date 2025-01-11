from datetime import datetime, timedelta
from typing import Dict


def get_detailed_day_report(day: Dict[str, any]) -> str:
        return f"""
{day['time']}
Температура: от {day['temperature_2m_max']}°C до {day['temperature_2m_min']}°C
Ощущается как: от {day['apparent_temperature_max']}°C до {day['apparent_temperature_min']}°C
Порывы ветра до: {day['wind_gusts_10m_max']} км/ч
Скорость ветра до: {day['wind_speed_10m_max']} км/ч
Восход: {datetime.fromisoformat(day['sunrise']) + timedelta(hours=2)}
Закат: {datetime.fromisoformat(day['sunset']) + timedelta(hours=2)}
Осадков за день: {day['precipitation_hours']} часов
Общее количество осадков: {day['precipitation_sum']} мм
"""

def get_short_day_report(day: Dict[str, any]):
        return f"""
{day['time']}
Температура: от {day['temperature_2m_max']}°C до {day['temperature_2m_min']}°C
Ощущается как: от {day['apparent_temperature_max']}°C до {day['apparent_temperature_min']}°C
Осадков за день: {day['precipitation_hours']} часов
Общее количество осадков: {day['precipitation_sum']} мм
"""

def parse_weather_now(current_weather: Dict[str, any]) -> str:
        return f"""
Сейчас
Температура: {current_weather['temperature']}°C
Скорость ветра: {current_weather['wind_speed']} м/с
"""
