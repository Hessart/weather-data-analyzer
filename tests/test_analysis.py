
import unittest
import pandas as pd
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch

from analysis import (
    load_data,
    analyze_temperature,
    analyze_humidity,
    analyze_comfortable_weather
)


class TestWeatherAnalysis(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "city": ["Sanok", "Ateny", "Barcelona"],
            "country": ["Polska", "Grecja", "Hiszpania"],
            "temperature": [8.6, 20.4, 23.4],
            "humidity": [91, 67, 55],
            "wind_speed": [4.0, 8.9, 9.1]
        })

    def test_temperature_analysis(self):
        output = StringIO()

        with redirect_stdout(output):
            analyze_temperature(self.df)

        result = output.getvalue()

        self.assertIn("17.47", result)
        self.assertIn("Barcelona", result)
        self.assertIn("Sanok", result)

    def test_humidity_analysis(self):
        output = StringIO()

        with redirect_stdout(output):
            analyze_humidity(self.df)

        result = output.getvalue()

        self.assertIn("Sanok", result)
        self.assertIn("91", result)

    def test_comfortable_weather(self):
        output = StringIO()

        with redirect_stdout(output):
            analyze_comfortable_weather(self.df)

        result = output.getvalue()

        self.assertIn("Ateny", result)
        self.assertIn("Barcelona", result)
        self.assertNotIn("Sanok", result)
   
    
    def test_missing_columns(self):
        invalid_data = pd.DataFrame({
            "city": ["Sanok"],
            "temperature": [8.6]
        })

        with patch("analysis.Path.exists", return_value=True):
            with patch("analysis.pd.read_csv", return_value=invalid_data):

                output = StringIO()

                with redirect_stdout(output):
                    result = load_data()

        self.assertIsNone(result)
        self.assertIn(
            "missing required columns",
            output.getvalue()
        )

    def test_empty_csv(self):
        with patch("analysis.Path.exists", return_value=True):
            with patch(
                "analysis.pd.read_csv",
                side_effect=pd.errors.EmptyDataError
            ):
                output = StringIO()

                with redirect_stdout(output):
                    result = load_data()

        self.assertIsNone(result)
        self.assertIn(
            "contains no data",
            output.getvalue()
        )

    
    def test_invalid_numeric_values(self):
        invalid_data = pd.DataFrame({
            "timestamp": ["2026-11-19 12:00:00"],
            "city": ["Sanok"],
            "country": ["Polska"],
            "temperature": ["invalid"],
            "humidity": [90],
            "wind_speed": [4.0]
        })

        with patch("analysis.Path.exists", return_value=True):
            with patch("analysis.pd.read_csv", return_value=invalid_data):

                output = StringIO()

                with redirect_stdout(output):
                    result = load_data()

        self.assertIsNone(result)
        self.assertIn(
            "invalid numeric values",
            output.getvalue()
        )


    def test_missing_file(self):
        with patch("analysis.Path.exists", return_value=False):

            output = StringIO()

            with redirect_stdout(output):
                result = load_data()

        self.assertIsNone(result)
        self.assertIn(
            "file not found",
            output.getvalue()
        )



if __name__ == "__main__":
    unittest.main()
