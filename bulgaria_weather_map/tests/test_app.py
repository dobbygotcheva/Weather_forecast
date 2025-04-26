"""
Tests for the Bulgaria Weather Map application.
"""
import unittest
import json
from unittest.mock import patch
from bulgaria_weather_map import create_app
from bulgaria_weather_map.models.cities import CITIES

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test that the home page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bulgaria Weather Map', response.data)

    @patch('bulgaria_weather_map.utils.weather.requests.get')
    def test_weather_api(self, mock_get):
        """Test that the weather API returns data in the expected format."""
        # Mock the OpenWeatherMap API response
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'main': {'temp': 20, 'humidity': 50, 'pressure': 1015, 'feels_like': 19.5},
            'weather': [{'main': 'Clear'}],
            'wind': {'speed': 3.5}
        }
        mock_get.return_value = mock_response

        # Set environment variable to use real API (which will be mocked)
        with patch('bulgaria_weather_map.utils.weather.USE_REAL_API', True):
            with patch('bulgaria_weather_map.utils.weather.OPENWEATHER_API_KEY', 'test_key'):
                response = self.client.get('/api/weather')
                self.assertEqual(response.status_code, 200)

                # Parse the JSON response
                data = json.loads(response.data)

                # Check that we have data for all cities
                self.assertEqual(len(data), len(CITIES))

                # Check the structure of the data for a sample city
                sample_city = list(data.keys())[0]
                self.assertIn('coordinates', data[sample_city])
                self.assertIn('temperature', data[sample_city])
                self.assertIn('condition', data[sample_city])
                self.assertIn('humidity', data[sample_city])
                self.assertIn('wind_speed', data[sample_city])
                self.assertIn('pressure', data[sample_city])
                self.assertIn('feels_like', data[sample_city])
                self.assertIn('timestamp', data[sample_city])

                # Check that coordinates is a list of two numbers
                self.assertEqual(len(data[sample_city]['coordinates']), 2)

                # Check that temperature is a string (either ending with °C or "N/A")
                self.assertTrue(
                    data[sample_city]['temperature'].endswith('°C') or 
                    data[sample_city]['temperature'] == 'N/A'
                )

                # Check that condition is a non-empty string
                self.assertTrue(isinstance(data[sample_city]['condition'], str))
                self.assertTrue(len(data[sample_city]['condition']) > 0)

    def test_debug_endpoint(self):
        """Test that the debug endpoint returns the expected information."""
        response = self.client.get('/debug')
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.data)
        
        # Check that the debug info contains the expected keys
        self.assertIn('app_running', data)
        self.assertIn('routes', data)
        self.assertIn('static_folder', data)
        self.assertIn('template_folder', data)
        self.assertIn('environment_vars', data)
        self.assertIn('cities_count', data)
        self.assertIn('openlayers_available', data)
        
        # Check that app_running is True
        self.assertTrue(data['app_running'])
        
        # Check that cities_count matches the number of cities in the CITIES dictionary
        self.assertEqual(data['cities_count'], len(CITIES))

    def test_api_test_endpoint(self):
        """Test that the API test endpoint returns the expected response."""
        response = self.client.get('/api/test')
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.data)
        
        # Check that the response contains the expected keys and values
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertEqual(data['status'], 'API is working')
        self.assertEqual(data['message'], 'If you see this, the API is functional')

if __name__ == '__main__':
    unittest.main()