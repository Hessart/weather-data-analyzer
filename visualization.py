
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_temperature(df):
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        df["city"],
        df["temperature"]
    )

    plt.title("Temperature by City")
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")

    # Display temperature values above bars
    plt.bar_label(bars, fmt="%.1f °C", padding=3)

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(
        Path(__file__).parent / "data" / "temperature_chart.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


def plot_humidity(df):
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        df["city"],
        df["humidity"]
    )

    plt.title("Humidity by City")
    plt.xlabel("City")
    plt.ylabel("Humidity (%)")

    plt.bar_label(bars, fmt="%.0f%%", padding=3)

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(
        Path(__file__).parent / "data" / "humidity_chart.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


def plot_temperature_history(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure(figsize=(12, 6))

    for city in df["city"].unique():
        city_data = df[df["city"] == city]

        plt.plot(
            city_data["timestamp"],
            city_data["temperature"],
            marker="o",
            label=city
        )

    plt.title("Temperature Changes Over Time")
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (°C)")

    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(
        Path(__file__).parent / "data" / "temperature_history_chart.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()



