def get_weather_icon_openweather(description):
    if "clear sky" in description.lower():
        return "weather/icons/sun.png"
    if "few clouds" in description.lower():
        return "weather/icons/sun-behind-small-cloud.png"
    if "scattered clouds" in description.lower():
        return "weather/icons/sun-behind-large-cloud.png"
    if "broken clouds" in description.lower():
        return "weather/icons/cloud.png"
    if "shower rain" in description.lower():
        return "weather/icons/sun-behind-rain-cloud.png"
    if "rain" in description.lower():
        return "weather/icons/rain.png"
    if "thunderstorm" in description.lower():
        return "weather/icons/cloud-with-lightning.png"
    if "snow" in description.lower():
        return "weather/icons/snow.png"
    if "mist" or "fog" in description.lower():
        return "weather/icons/fog.png"
    else:
        return "weather/icons/bomb.png"
