
import unittest
import requests
from unittest.mock import patch, Mock
from contextlib import redirect_stdout
from io import StringIO

from main import get_coordinates, get_weather

class TestWeatherAPI(unittest.TestCase):

    @patch("main.requests.get")
    def test_get_coordinates_success(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "results": [
                {
                    "name": "Sanok",
                    "country": "Polska",
                    "latitude": 49.56,
                    "longitude": 22.20
                }
            ]
        }

        mock_get.return_value = mock_response

        result = get_coordinates("Sanok")

        self.assertEqual(result["name"], "Sanok")
        self.assertEqual(result["country"], "Polska")
        self.assertEqual(result["latitude"], 49.56)
        self.assertEqual(result["longitude"], 22.20)


    @patch("main.requests.get")
    def test_get_coordinates_not_found(self, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = {}

        mock_get.return_value = mock_response

        result = get_coordinates("NieistniejaceMiasto")

        self.assertIsNone(result)


    @patch("main.requests.get")
    def test_get_coordinates_connection_error(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError

        output = StringIO()

        with redirect_stdout(output):
            result = get_coordinates("Sanok")

        self.assertIsNone(result)
        self.assertIn("Connection error", output.getvalue())


    @patch("main.requests.get")
    def test_get_weather_success(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 8.6,
                "relative_humidity_2m": 91,
                "wind_speed_10m": 4.0
            }
        }

        mock_get.return_value = mock_response

        result = get_weather(49.56, 22.20)

        self.assertEqual(result["temperature_2m"], 8.6)
        self.assertEqual(result["relative_humidity_2m"], 91)
        self.assertEqual(result["wind_speed_10m"], 4.0)


    @patch("main.requests.get")
    def test_get_weather_connection_error(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError

        output = StringIO()

        with redirect_stdout(output):
            result = get_weather(49.56, 22.20)

        self.assertIsNone(result)
        self.assertIn(
            "Weather API error",
            output.getvalue()
        )

if __name__ == "__main__":
    unittest.main()