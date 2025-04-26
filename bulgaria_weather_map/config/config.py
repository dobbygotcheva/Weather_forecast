"""
Configuration settings for the Bulgaria Weather Map application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your_api_key_here')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Weather conditions mapping (for reference)
WEATHER_CONDITIONS = ["Clear", "Clouds", "Rain", "Snow", "Mist", "Thunderstorm"]

# Application configuration
DEBUG = True
USE_REAL_API = os.environ.get('USE_REAL_API', 'true').lower() == 'true'