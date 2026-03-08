# CORRECTED weather_service.py
import requests
import os

api_key = "cae50eaff9a5304911b66c61213e1c7d"

# Get weather data using OpenWeatherMap API
def get_weather(city_name):
    # CORRECTION: Fixed the base URL format
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            rainfall = data.get('rain', {}).get('1h', 0)  # 0 if no rainfall data
            return {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall
            }
        else:
            return {"error": data.get("message", "Unable to fetch weather data")}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    city = "Delhi"
    weather = get_weather(city)
    print(f"🌤 Weather in {city}: {weather}")