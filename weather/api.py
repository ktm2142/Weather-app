import requests
from django.conf import settings


class WeatherAPI:
    @staticmethod
    def get_weather_data(city_name):
        url = f"{settings.VISUALCROSSING_BASE_URL}/{city_name}"
        params = {
            "unitGroup": "metric",
            "key": settings.VISUALCROSSING_API_KEY,
            "contentType": "json"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    @staticmethod
    def parse_current_conditions(data):
        if not data:
            return None
        current = data.get("currentConditions", {})
        return {
            'temperature': current.get('temp', 0),
            'weather_text': current.get('conditions', ''),
            'humidity': current.get('humidity', 0),
            'wind_speed': current.get('windspeed', 0),
            'uv_index': current.get('uvindex', 0),
        }

    @staticmethod
    def parse_forecast(data):
        if not data:
            return []
        return [{
            'date': day.get('datetime'),
            'min_temperature': day.get('tempmin', 0),
            'max_temperature': day.get('tempmax', 0),
            'weather_phrase': day.get('conditions', '')
        } for day in data.get("days", [])[:5]]


class ImageAPI:
    @staticmethod
    def get_city_image(city_name):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": settings.GOOGLE_API_KEY,
            "cx": settings.GOOGLE_CSE_ID,
            "q": f"{city_name} city",
            "searchType": "image",
            "imgSize": "large",
            "num": 1
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0]["link"]
        except requests.RequestException:
            pass
        return None