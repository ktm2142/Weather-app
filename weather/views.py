from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import City, CurrentWeather, DailyForecast, CityImage
from .api import WeatherAPI, ImageAPI


def weather_view(request):
    city_name = request.GET.get('city', '')
    context = {}

    if city_name:
        city, _ = City.objects.get_or_create(name=city_name)

        current_weather = CurrentWeather.objects.filter(
            city=city,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).first()

        if current_weather:
            forecast = DailyForecast.objects.filter(city=city, date__gte=timezone.now().date())[:5]
        else:
            weather_data = WeatherAPI.get_weather_data(city_name)
            if weather_data:
                current_conditions = WeatherAPI.parse_current_conditions(weather_data)
                forecast_data = WeatherAPI.parse_forecast(weather_data)

                CurrentWeather.objects.update_or_create(
                    city=city,
                    defaults={
                        'temperature': current_conditions['temperature'],
                        'weather_text': current_conditions['weather_text'],
                        'humidity': current_conditions['humidity'],
                        'wind_speed': current_conditions['wind_speed'],
                        'uv_index': current_conditions['uv_index'],
                        'timestamp': timezone.now()
                    }
                )

                DailyForecast.objects.filter(city=city).delete()
                for day in forecast_data:
                    DailyForecast.objects.create(
                        city=city,
                        date=day['date'],
                        min_temperature=day['min_temperature'],
                        max_temperature=day['max_temperature'],
                        weather_phrase=day['weather_phrase']
                    )

                current_weather = CurrentWeather.objects.get(city=city)
                forecast = DailyForecast.objects.filter(city=city)[:5]
            else:
                context['error'] = f"City '{city_name}' not found"

        if 'error' not in context:
            city_image, created = CityImage.objects.get_or_create(city=city)
            if created or not city_image.image_url:
                image_url = ImageAPI.get_city_image(city_name)
                if image_url:
                    city_image.image_url = image_url
                    city_image.save()

            context = {
                'city_name': city_name,
                'current_conditions': current_weather,
                'forecast': forecast,
                'city_image': city_image.image_url if city_image.image_url else None
            }

    return render(request, 'weather/weather.html', context)