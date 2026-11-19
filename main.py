import requests

import csv
from datetime import datetime
from pathlib import Path

from analysis import (
    load_data,
    analyze_temperature,
    analyze_humidity,
    analyze_comfortable_weather
)

from visualization import (
    plot_temperature,
    plot_humidity,
    plot_temperature_history
)


def get_coordinates(city):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "pl",
        "format": "json"
    }

    try:
        response = requests.get(
            geocoding_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        print(f"Connection error: {error}")
        return None

    if "results" not in data:
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "country": location.get("country", "Unknown"),
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


def get_weather(latitude, longitude):
    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    try:
        response = requests.get(
            weather_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        return data["current"]

    except requests.exceptions.RequestException as error:
        print(f"Weather API error: {error}")
        return None


def display_weather(location, weather):
    print("==============================")
    print("      WEATHER DATA ANALYZER")
    print("==============================")

    print(f"City:        {location['name']}")
    print(f"Country:     {location['country']}")
    print(f"Temperature: {weather['temperature_2m']} °C")
    print(f"Humidity:    {weather['relative_humidity_2m']} %")
    print(f"Wind speed:  {weather['wind_speed_10m']} km/h")

    print("==============================")


def save_weather(location, weather):
    file_path = Path(__file__).parent / "weather_history.csv"

    file_exists = file_path.exists()

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        if not file_exists:
            writer.writerow([
                "timestamp",
                "city",
                "country",
                "temperature",
                "humidity",
                "wind_speed"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            location["name"],
            location["country"],
            str(weather["temperature_2m"]).replace(".", ","),
            weather["relative_humidity_2m"],
            str(weather["wind_speed_10m"]).replace(".", ",")
        ])

    print("Weather data saved successfully.")


def main():
    city = input("Enter city name: ")

    location = get_coordinates(city)

    if location is None:
        print("City not found.")
        return

    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather is None:
        print("Could not retrieve weather data.")
        return

    display_weather(location, weather)
    save_weather(location, weather)
     # Load historical weather data
    df = load_data()

    if df is None:
        return

    # Weather analysis
    analyze_temperature(df)
    analyze_humidity(df)
    analyze_comfortable_weather(df)

    # Data visualization
    plot_temperature(df)
    plot_humidity(df)
    plot_temperature_history(df)


if __name__ == "__main__":


    main()