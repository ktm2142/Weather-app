from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CurrentWeather(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    weather_text = models.CharField(max_length=100)
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    uv_index = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C, {self.weather_text}"


class DailyForecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    weather_phrase = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city.name} - {self.date}: {self.min_temperature}°C to {self.max_temperature}°C"


class CityImage(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.city.name}"