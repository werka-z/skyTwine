from celery import shared_task
from .services import fetch_openweather_data, fetch_weatherapi_data, process_openweather_data, process_weatherapi_data
from decouple import config
from .models import Weather
from .assign import assign_image, assign_sky_condition


country = config('COUNTRY')
city_en = config('CITY_EN')
city = config('CITY_PL')


# Executes daily: fetches and processes data, calculates and creates the average model
@shared_task
def hourly_updates():

    raw_data_ow = fetch_openweather_data(city)
    if raw_data_ow:
        process_openweather_data(raw_data_ow)

    raw_data_wa = fetch_weatherapi_data(city_en)
    if raw_data_wa:
        process_weatherapi_data(raw_data_wa)

    for i in range(1, 4):

        # Get attribute
        ow = getattr(Weather.custom_objects, f'ow_{i}')()
        wa = getattr(Weather.custom_objects, f'wa_{i}')()

        if ow and wa:
            avg_skycon = assign_sky_condition(ow.sky_condition, wa.sky_condition)
            avg_temp = round((ow.temperature + wa.temperature) / 2, 1)
            avg_wind_speed = round((ow.wind_speed + wa.wind_speed) / 2, 1)
            avg_pressure = int((ow.pressure + wa.pressure) / 2)
            avg_humidity = int((ow.humidity + wa.humidity) / 2)
            avg_image = assign_image(avg_skycon)

            Weather.custom_objects.create(
                    date=ow.date,
                    city=city,
                    country=country,
                    sky_condition=avg_skycon,
                    temperature=avg_temp,
                    wind_speed=avg_wind_speed,
                    pressure=avg_pressure,
                    humidity=avg_humidity,
                    source='average',
                    image=avg_image
                )
