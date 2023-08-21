import requests
import logging
from decouple import config
from .models import Weather
from .assign import assign_image


logger = logging.getLogger(__name__)

api_key_openweather = config('OPENWEATHER_API_KEY')
api_key_weatherapi = config('WEATHERAPI_API_KEY')
country = config('COUNTRY')
city_pl = config('CITY_PL')


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
        logger.error("Error when fetching openweather data for city: %s", city)
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
        logger.error("Error when fetching weatherapi data for city: %s", city)
        return None


def process_openweather_data(data):
    # print(data)
    # print("OK")

    if "list" not in data:
        raise Exception("The 'list' key does not exist in the data dictionary.")

    hours_of_interest = ["09:00:00", "12:00:00", "15:00:00", "18:00:00"]  # We want hours within the proper daytime
    days = {}  # Dictionary where keys are "YYYY-MM-DD" and values are other dictionaries

    for forecast in data['list']:
        day = forecast['dt_txt'].split()[0]
        time = forecast['dt_txt'].split()[1]

        if time in hours_of_interest:

            if day not in days:  # Adding following days
                days[day] = {
                    "temps": [],
                    "sky_conditions": [],
                    "wind_speeds": [],
                    "pressures": [],
                    "humidities": []
                }

            temp = forecast['main']['temp'] - 273.15
            sky_condition = forecast['weather'][0]['description']
            wind_speed = forecast['wind']['speed']
            pressure = forecast['main']['pressure']
            humidity = forecast['main']['humidity']

            days[day]["temps"].append(temp)
            days[day]["sky_conditions"].append(sky_condition)
            days[day]["wind_speeds"].append(wind_speed)
            days[day]["pressures"].append(pressure)
            days[day]["humidities"].append(humidity)

    # Calculating the averages for each day and creating an instance of the Weather model
    for day, values in days.items():
        avg_temp = round(sum(values["temps"]) / len(values["temps"]), 1)
        avg_sky_condition = max(set(values["sky_conditions"]), key=values["sky_conditions"].count)
        avg_wind_speed = round(sum(values["wind_speeds"]) / len(values["wind_speeds"]), 1)
        avg_pressure = int(sum(values["pressures"]) / len(values["pressures"]))
        avg_humidity = int(sum(values["humidities"]) / len(values["humidities"]))

        Weather.custom_objects.create(
            date=day,
            city=city_pl,
            country=country,
            sky_condition=avg_sky_condition,
            temperature=avg_temp,
            wind_speed=avg_wind_speed,
            pressure=int(avg_pressure),
            humidity=avg_humidity,
            source='openweather',
            image=assign_image(avg_sky_condition)
        )


def process_weatherapi_data(data):

    for day in data["forecast"]["forecastday"]:
        Weather.custom_objects.create(
            date=day["date"],
            city=city_pl,
            country=country,
            sky_condition=day["day"]["condition"]["text"].lower(),
            temperature=day["day"]["avgtemp_c"],
            wind_speed=day["day"]["maxwind_kph"],
            pressure=1013,
            humidity=day["day"]["avghumidity"],
            source='weatherapi',
            image=assign_image(day["day"]["condition"]["text"], )
        )
    return None
