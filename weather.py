
import requests


def get_weather(city):

    # Find the city's coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        geo_response = requests.get(
            geo_url, params=geo_params, timeout=15
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        locations = geo_data.get("results", [])

        if not locations:
            return {"error": "Location not found. Check the city name."}

        place = locations[0]

        latitude = place["latitude"]
        longitude = place["longitude"]

        # Fetch current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation"
            ),
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url, params=weather_params, timeout=15
        )
        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        return {
            "city": place["name"],
            "country": place.get("country", ""),
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "rainfall": current["precipitation"],
            "time": current["time"]
        }

    except requests.RequestException:
        return {"error": "Weather service unavailable. Try again."}

    except (KeyError, ValueError, TypeError):
        return {"error": "Could not read weather information."}
