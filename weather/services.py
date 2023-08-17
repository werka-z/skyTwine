import requests
from decouple import config
from .models import Weather
from celery import shared_task

api_key_openweather = config('OPENWEATHER_API_KEY')
api_key_weatherapi = config('WEATHERAPI_API_KEY')
country = config('COUNTRY')


def process_openweather_data(city, data):
    hours_of_interest = ["12:00:00", "15:00:00", "18:00:00"]  # We want hours within the proper daytime
    day_data = {}  # Dictionary where keys are "YYYY-MM-DD" and values are other dictionaries

    for forecast in data["list"]:
        date = forecast["dt_txt"].split()[0]
        time = forecast["dt_txt"].split()[1]

        if time in hours_of_interest:
            if date not in day_data:  # Adding following days
                day_data[date] = {
                    "temps": [],
                    "sky_conditions": [],
                    "wind_speeds": [],
                    "pressures": [],
                    "humidities": []
                }

            temp = forecast["main"]["temp"] - 273.15  # Kelvin to Celsius
            sky_condition = forecast["weather"][0]["description"]
            wind_speed = forecast["wind"]["speed"]
            pressure = forecast["main"]["pressure"]
            humidity = forecast["main"]["humidity"]

            day_data[date]["temps"].append(temp)
            day_data[date]["sky_conditions"].append(sky_condition)
            day_data[date]["wind_speeds"].append(wind_speed)
            day_data[date]["pressures"].append(pressure)
            day_data[date]["humidities"].append(humidity)

    # Calculating the averages for each day and creating an instance of the Weather model
    for date, values in day_data.items():
        avg_temp = sum(values["temps"]) / len(values["temps"])
        avg_sky_condition = max(set(values["sky_conditions"]),
                                key=values["sky_conditions"].count)  # Most frequent condition
        avg_wind_speed = sum(values["wind_speeds"]) / len(values["wind_speeds"])
        avg_pressure = sum(values["pressures"]) / len(values["pressures"])
        avg_humidity = sum(values["humidities"]) / len(values["humidities"])

        Weather.objects.create(
            city=city,
            country=f"{country}",
            sky_condition=avg_sky_condition,
            temperature=avg_temp,
            wind_speed=avg_wind_speed,
            pressure=int(avg_pressure),
            humidity=avg_humidity,
            source='openweather'
        )


def fetch_openweather_data(city):
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key_openweather}"

    params = {
        "q": f"{city},pl",
        "APPID": api_key_openweather
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_weatherapi_data(city, days=3):
    api_url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key_weatherapi}&q={city}&days={days}&aqi=no" \
              f"&alerts=no"

    params = {
        'access_key': api_key_weatherapi,
        'query': city,
        'forecast_days': days,
        'hourly': 1
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def process_weatherapi_data(city, data):

    for day in data["forecast"]["forecastday"]:
        Weather.objects.create(
            city=city,
            country=country,
            sky_condition=day["day"]["condition"]["text"],
            temperature=day["day"]["avgtemp_c"],
            wind_speed=day["day"]["maxwind_mph"],
            pressure=1013,
            source='weatherapi'
        )
    return None


@shared_task
def daily_updates(city):
    raw_data_1 = fetch_openweather_data(city)
    if raw_data_1:
        process_openweather_data(city, raw_data_1)

    raw_data_2 = fetch_weatherapi_data(city)
    if raw_data_2:
        process_weatherapi_data(city, raw_data_2)

    openweather_data = Weather.objects.filter(city=city, source='openweather')
    weatherapi_data = Weather.objects.filter(city=city, source='weatherapi')



