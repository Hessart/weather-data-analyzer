import unittest
import pandas as pd
import matplotlib.pyplot as plt

from unittest.mock import patch
from visualization import ( 
    plot_temperature, 
    plot_humidity, 
    plot_temperature_history
)

class TestVisualization(unittest.TestCase):

    def test_plot_temperature(self):

        df = pd.DataFrame({
            "city": ["Sanok", "Ateny", "Barcelona"],
            "temperature": [8.6, 20.4, 23.4]
        })

        with patch("visualization.plt.savefig") as mock_savefig:
            with patch("visualization.plt.show") as mock_show:

                plot_temperature(df)

        mock_savefig.assert_called_once()
        mock_show.assert_called_once()

        saved_path = str(mock_savefig.call_args[0][0])

        self.assertTrue(
            saved_path.endswith("temperature_chart.png")
        )

        plt.close("all")


    @patch("visualization.plt.savefig")
    @patch("visualization.plt.show")
    def test_plot_humidity(self, mock_show, mock_savefig):

        df = pd.DataFrame({
            "city": ["Sanok", "Ateny", "Barcelona"],
            "humidity": [91, 67, 55]
        })

        plot_humidity(df)

        mock_savefig.assert_called_once()
        mock_show.assert_called_once()

        saved_path = str(mock_savefig.call_args[0][0])

        self.assertTrue(
            saved_path.endswith("humidity_chart.png")
        )

        plt.close("all")

    @patch("visualization.plt.savefig")
    @patch("visualization.plt.show")
    def test_plot_temperature_history(self, mock_show, mock_savefig):

        df = pd.DataFrame({
            "timestamp": [
                "2026-11-18 12:00:00",
                "2026-11-18 12:05:00",
                "2026-11-18 12:00:00",
                "2026-11-18 12:05:00"
            ],
            "city": [
                "Sanok",
                "Sanok",
                "Barcelona",
                "Barcelona"
            ],
            "temperature": [8.6, 9.2, 23.4, 24.1]
        })

        plot_temperature_history(df)

        mock_savefig.assert_called_once()
        mock_show.assert_called_once()

        saved_path = str(mock_savefig.call_args[0][0])

        self.assertTrue(
            saved_path.endswith("temperature_history_chart.png")
        )

        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(df["timestamp"])
        )

        plt.close("all")

if __name__ == "__main__":
    unittest.main()
