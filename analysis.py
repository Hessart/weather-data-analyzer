
import pandas as pd
from pathlib import Path


def load_data():
    file_path = Path(__file__).parent / "weather_history.csv"

    if not file_path.exists():
        print("Error: Weather history file not found.")
        return None

    try:
        df = pd.read_csv(file_path, sep=";", decimal=",")
    except pd.errors.EmptyDataError:
        print("Error: CSV file contains no data.")
        return None
    except pd.errors.ParserError:
        print("Error: CSV file has an invalid format.")
        return None
    except UnicodeDecodeError:
        print("Error: CSV file encoding is invalid.")
        return None

    required_columns = [
        "timestamp",
        "city",
        "country",
        "temperature",
        "humidity",
        "wind_speed"
    ]

    if not all(column in df.columns for column in required_columns):
        print("Error: CSV file is missing required columns.")
        return None
    
    if df.empty:
        print("Error: Weather history file is empty.")
        return None

    numeric_columns = [
        "temperature",
        "humidity",
        "wind_speed"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[numeric_columns].isna().any().any():
        print("Error: CSV contains invalid numeric values.")
        return None

    return df


def analyze_temperature(df):
    print("\n--- WEATHER ANALYSIS ---")

    average_temperature = df["temperature"].mean()
    highest_temperature = df["temperature"].max()
    lowest_temperature = df["temperature"].min()

    print(f"Average temperature: {average_temperature:.2f} °C")
    print(f"Highest temperature: {highest_temperature} °C")
    print(f"Lowest temperature: {lowest_temperature} °C")

    warmest_city = df.loc[df["temperature"].idxmax()]
    coldest_city = df.loc[df["temperature"].idxmin()]

    print("\n--- CITY ANALYSIS ---")

    print(
        f"Warmest city: {warmest_city['city']} "
        f"({warmest_city['temperature']} °C)"
    )

    print(
        f"Coldest city: {coldest_city['city']} "
        f"({coldest_city['temperature']} °C)"
    )


def analyze_humidity(df):
    print("\n--- HUMIDITY ABOVE 70% ---")

    humid_cities = df[df["humidity"] > 70]

    print(humid_cities)

    print("\n--- HUMIDITY RANKING ---")

    sorted_cities = df.sort_values(
        by="humidity",
        ascending=False
    )

    print(sorted_cities[["city", "country", "humidity"]])


def analyze_comfortable_weather(df):
    print("\n--- COMFORTABLE WEATHER ---")

    comfortable_cities = df[
        (df["temperature"] > 20) &
        (df["humidity"] < 70)
    ]

    print(
        comfortable_cities[
            ["city", "country", "temperature", "humidity"]
        ]
    )


def main():
    df = load_data()

    if df is None:
        return

    analyze_temperature(df)
    analyze_humidity(df)
    analyze_comfortable_weather(df)


if __name__ == "__main__":
    main()
