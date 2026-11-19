import unittest
import csv
import tempfile

from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from main import save_weather


class TestWeatherStorage(unittest.TestCase):

    def test_save_weather_creates_csv(self):

        location = {
            "name": "Sanok",
            "country": "Polska"
        }

        weather = {
            "temperature_2m": 8.6,
            "relative_humidity_2m": 91,
            "wind_speed_10m": 4.0
        }

        with tempfile.TemporaryDirectory() as temp_dir:

            fake_main = Path(temp_dir) / "main.py"

            with patch("main.__file__", str(fake_main)):

                output = StringIO()

                with redirect_stdout(output):
                    save_weather(location, weather)

            file_path = Path(temp_dir) / "weather_history.csv"

            self.assertTrue(file_path.exists())

            with open(file_path, newline="", encoding="utf-8") as file:
                reader = list(csv.reader(file, delimiter=";"))

            self.assertEqual(
                reader[0],
                ["timestamp", "city", "country",
                 "temperature", "humidity", "wind_speed"]
            )

            self.assertEqual(reader[1][1], "Sanok")
            self.assertEqual(reader[1][2], "Polska")
            self.assertEqual(reader[1][3], "8,6")
            self.assertEqual(reader[1][4], "91")
            self.assertEqual(reader[1][5], "4,0")

            self.assertIn(
                "saved successfully",
                output.getvalue()
            )

    def test_save_weather_appends_new_measurement(self):

        location = {
            "name": "Barcelona",
            "country": "Hiszpania"
        }

        weather = {
            "temperature_2m": 23.4,
            "relative_humidity_2m": 55,
            "wind_speed_10m": 9.1
        }

        with tempfile.TemporaryDirectory() as temp_dir:

            fake_main = Path(temp_dir) / "main.py"

            with patch("main.__file__", str(fake_main)):

                with redirect_stdout(StringIO()):
                    save_weather(location, weather)
                    save_weather(location, weather)

            file_path = Path(temp_dir) / "weather_history.csv"

            with open(file_path, newline="", encoding="utf-8") as file:
                reader = list(csv.reader(file, delimiter=";"))

            self.assertEqual(len(reader), 3)
            self.assertEqual(reader[1][1], "Barcelona")
            self.assertEqual(reader[2][1], "Barcelona")
    
    def test_csv_header_is_not_duplicated(self):

        location = {
            "name": "Sanok",
            "country": "Polska"
        }

        weather = {
            "temperature_2m": 8.6,
            "relative_humidity_2m": 91,
            "wind_speed_10m": 4.0
        }

        with tempfile.TemporaryDirectory() as temp_dir:

            fake_main = Path(temp_dir) / "main.py"

            with patch("main.__file__", str(fake_main)):
                with redirect_stdout(StringIO()):
                    save_weather(location, weather)
                    save_weather(location, weather)
                    save_weather(location, weather)

            file_path = Path(temp_dir) / "weather_history.csv"

            with open(file_path, newline="", encoding="utf-8") as file:
                reader = list(csv.reader(file, delimiter=";"))

            self.assertEqual(len(reader), 4)

            self.assertEqual(
                reader[0][0],
                "timestamp"
            )

            self.assertEqual(
                sum(row[0] == "timestamp" for row in reader),
                1
            )

    def test_save_weather_handles_file_error(self):

        location = {
            "name": "Sanok",
            "country": "Polska"
        }

        weather = {
            "temperature_2m": 8.6,
            "relative_humidity_2m": 91,
            "wind_speed_10m": 4.0
        }

        with patch("main.Path.exists", return_value=False):
            with patch("builtins.open", side_effect=PermissionError):

                with self.assertRaises(PermissionError):
                    save_weather(location, weather)





if __name__ == "__main__":
    unittest.main()
