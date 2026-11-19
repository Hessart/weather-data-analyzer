import unittest
from unittest.mock import patch
import pandas as pd

from main import main

class TestMain(unittest.TestCase):

    @patch("main.plot_temperature_history")
    @patch("main.plot_humidity")
    @patch("main.plot_temperature")
    @patch("main.analyze_comfortable_weather")
    @patch("main.analyze_humidity")
    @patch("main.analyze_temperature")
    @patch("main.load_data")
    def test_main_execution(
        self,
        mock_load,
        mock_temperature,
        mock_humidity,
        mock_comfortable,
        mock_plot_temperature,
        mock_plot_humidity,
        mock_plot_history
    ):

        mock_load.return_value = pd.DataFrame({
            "city": ["Sanok"],
            "country": ["Polska"],
            "temperature": [8.6],
            "humidity": [91],
            "wind_speed": [4.0],
            "timestamp": ["2026-11-19 12:00:00"]
        })

        main()

        mock_load.assert_called_once()
        mock_temperature.assert_called_once()
        mock_humidity.assert_called_once()
        mock_comfortable.assert_called_once()

        mock_plot_temperature.assert_called_once()
        mock_plot_humidity.assert_called_once()
        mock_plot_history.assert_called_once()


if __name__ == "__main__":
    unittest.main()
