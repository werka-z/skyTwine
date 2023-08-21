from django.db import models
from datetime import datetime, timedelta

today = datetime.today().date()
tomorrow = today + timedelta(days=1)
day_after_tomorrow = today + timedelta(days=2)


# The manager always gives access to the last created source and date specific weather instance
class WeatherManager(models.Manager):
    def ow_1(self):
        return self.filter(date=today, source='openweather').last()

    def ow_2(self):
        return self.filter(date=tomorrow, source='openweather').last()

    def ow_3(self):
        return self.filter(date=day_after_tomorrow, source='openweather').last()

    def wa_1(self):
        return self.filter(date=today, source='weatherapi').last()

    def wa_2(self):
        return self.filter(date=tomorrow, source='weatherapi').last()

    def wa_3(self):
        return self.filter(date=day_after_tomorrow, source='weatherapi').last()

    def av_1(self):
        return self.filter(date=today, source='average').last()

    def av_2(self):
        return self.filter(date=tomorrow, source='average').last()

    def av_3(self):
        return self.filter(date=day_after_tomorrow, source='average').last()


class Weather(models.Model):
    date = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    sky_condition = models.CharField(max_length=200)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=200)

    SOURCE_CHOICES = [
        ('openweather', 'OpenWeather'),
        ('weatherapi', 'WeatherAPI'),
        ('average', 'Average')
    ]
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)

    def __str__(self):
        return f"Weather data for {self.city}, {self.country}"

    custom_objects = WeatherManager()

    def debug_info(self):
        info = f"""
        Weather data for {self.city}, {self.country}:
        - Date: {self.date}
        - Sky Condition: {self.sky_condition}
        - Temperature: {self.temperature}°C
        - Wind Speed: {self.wind_speed} m/s
        - Pressure: {self.pressure} hPa
        - Humidity: {self.humidity if self.humidity else "N/A"}%
        - Image: {self.image}
        - Source: {self.get_source_display()}
        """
        return info
