from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    sky_condition = models.CharField(max_length=200)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.FloatField()

    SOURCE_CHOICES = [
        ('openweather', 'OpenWeather'),
        ('weatherapi', 'WeatherAPI')
    ]
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)

    def __str__(self):
        return f"Weather data for {self.city}, {self.country}"
