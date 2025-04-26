"""
Utility functions for generating and fetching weather data.
"""
import random
import requests
from datetime import datetime
from bulgaria_weather_map.models.cities import CITIES
from bulgaria_weather_map.config.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, USE_REAL_API

def generate_mock_weather_data():
    """
    Generate mock weather data for Bulgarian cities based on seasonal patterns.
    
    Returns:
        dict: Dictionary of weather data for each city
    """
    weather_data = {}
    
    # Get current month to determine seasonal temperatures
    current_month = datetime.now().month
    print(f"Current month: {current_month}")

    # Define seasonal temperature ranges for Bulgaria based on meteorological data
    # Bulgaria's climate varies with cold winters and warm summers
    if current_month in [12, 1, 2]:  # Winter (December-February)
        season = "Winter"
        min_temp = -5
        max_temp = 8
        condition_weights = {
            "Snow": 0.3,
            "Clouds": 0.4, 
            "Clear": 0.2,
            "Mist": 0.1,
            "Rain": 0.0,
            "Thunderstorm": 0.0
        }
    elif current_month in [3, 4, 5]:  # Spring (March-May)
        season = "Spring"
        min_temp = 8
        max_temp = 20
        condition_weights = {
            "Rain": 0.3,
            "Clouds": 0.3,
            "Clear": 0.3,
            "Mist": 0.05,
            "Thunderstorm": 0.05,
            "Snow": 0.0
        }
    elif current_month in [6, 7, 8]:  # Summer (June-August)
        season = "Summer"
        min_temp = 18
        max_temp = 32
        condition_weights = {
            "Clear": 0.5,
            "Clouds": 0.2,
            "Thunderstorm": 0.15,
            "Rain": 0.15,
            "Mist": 0.0,
            "Snow": 0.0
        }
    else:  # Fall (September-November)
        season = "Fall"
        min_temp = 5
        max_temp = 20
        condition_weights = {
            "Clouds": 0.4,
            "Rain": 0.3,
            "Clear": 0.2,
            "Mist": 0.1,
            "Thunderstorm": 0.0,
            "Snow": 0.0
        }

    print(f"Season: {season}, Temperature range: {min_temp}°C to {max_temp}°C")
    print(f"Weather conditions: {list(condition_weights.keys())}")

    # Generate realistic weather patterns across the region
    # Base temperature pattern that we'll modify for each city
    base_temp = min_temp + (max_temp - min_temp) * random.random()
    predominant_condition = random.choices(
        list(condition_weights.keys()),
        weights=list(condition_weights.values())
    )[0]

    print(f"Base temperature: {base_temp:.1f}°C, Predominant condition: {predominant_condition}")

    # Some regional variation to maintain consistency across nearby cities
    altitude_factor = 0.7  # Temperature drops with altitude
    coastal_factor = 1.2   # Coastal areas tend to be warmer in winter, cooler in summer

    for city, coords in CITIES.items():
        # Add slight city-specific variation
        # Higher altitude cities are cooler
        if city in ["Sofia", "Smolyan", "Gabrovo"]:
            temp_modifier = -2 * altitude_factor
        # Coastal cities have more moderate temperatures
        elif city in ["Varna", "Burgas"]:
            # Coastal cities are warmer in winter, cooler in summer
            if current_month in [12, 1, 2]:
                temp_modifier = 3 * coastal_factor
            elif current_month in [6, 7, 8]:
                temp_modifier = -3 * coastal_factor
            else:
                temp_modifier = 0
        else:
            temp_modifier = random.uniform(-1, 1)  # Small random variation

        # Calculate final temperature with realistic variation
        final_temp = round(base_temp + temp_modifier, 1)
        # Keep temperature within seasonal range
        final_temp = max(min_temp, min(max_temp, final_temp))

        # Slightly vary the condition for realism but maintain regional patterns
        if random.random() < 0.8:  # 80% chance to keep predominant condition
            condition = predominant_condition
        else:
            # Choose random alternative condition
            alternative_conditions = [c for c in condition_weights.keys() if c != predominant_condition and condition_weights[c] > 0]
            condition = random.choice(alternative_conditions) if alternative_conditions else predominant_condition

        # Generate additional mock weather parameters for more precision
        humidity = random.randint(30, 95)  # Humidity percentage
        wind_speed = round(random.uniform(0.5, 12.0), 1)  # Wind speed in m/s
        pressure = random.randint(990, 1030)  # Pressure in hPa
        feels_like = final_temp + random.uniform(-2.0, 2.0)  # Feels like temperature
        feels_like = round(max(min_temp, min(max_temp, feels_like)), 1)  # Keep within range

        # Get timestamp of data generation
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store the mock weather data - ensure coordinates are numerical values
        # OpenLayers expects [longitude, latitude] format
        weather_data[city] = {
            'coordinates': [float(coords['lon']), float(coords['lat'])],
            'temperature': f"{final_temp:.1f}°C",
            'condition': condition,
            'humidity': f"{humidity}%",
            'wind_speed': f"{wind_speed} m/s",
            'pressure': f"{pressure} hPa",
            'feels_like': f"{feels_like:.1f}°C",
            'timestamp': timestamp
        }

    # Print a sample of generated data
    sample_cities = list(CITIES.keys())[:3]  # First 3 cities
    print("Sample weather data generated:")
    for city in sample_cities:
        print(f"  {city}: {weather_data[city]['temperature']}, {weather_data[city]['condition']}")

    print(f"Total cities with weather data: {len(weather_data)}")
    return weather_data

def fetch_real_weather_data():
    """
    Fetch real weather data from OpenWeatherMap API.
    
    Returns:
        dict: Dictionary of weather data for each city
    """
    weather_data = {}
    
    for city, coords in CITIES.items():
        try:
            # Prepare parameters for OpenWeatherMap API request
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'  # Get temperature in Celsius
            }

            # Make API request to OpenWeatherMap
            response = requests.get(OPENWEATHER_BASE_URL, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse the response
            weather_data_response = response.json()

            # Extract temperature and weather condition with more precision
            temperature = weather_data_response['main']['temp']
            condition = weather_data_response['weather'][0]['main']

            # Extract additional weather parameters for more precision
            humidity = weather_data_response['main']['humidity']
            wind_speed = weather_data_response['wind']['speed']
            pressure = weather_data_response['main']['pressure']
            feels_like = weather_data_response['main']['feels_like']

            # Get timestamp of data retrieval
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Store the weather data - ensure consistent format with mock data
            weather_data[city] = {
                'coordinates': [float(coords['lon']), float(coords['lat'])],
                'temperature': f"{temperature:.1f}°C",
                'condition': condition,
                'humidity': f"{humidity}%",
                'wind_speed': f"{wind_speed} m/s",
                'pressure': f"{pressure} hPa",
                'feels_like': f"{feels_like:.1f}°C",
                'timestamp': timestamp
            }
        except Exception as e:
            # Log the error (in a production environment, you would use a proper logging system)
            print(f"Error fetching weather data for {city}: {str(e)}")

            # Fallback to a default value in case of error
            weather_data[city] = {
                'coordinates': [coords['lon'], coords['lat']],
                'temperature': "N/A",
                'condition': "Unknown"
            }
    
    return weather_data

def get_weather_data():
    """
    Get weather data, either mock or real depending on configuration.
    
    Returns:
        dict: Dictionary of weather data for each city
    """
    # Check if we should use real API or mock data
    has_valid_api_key = OPENWEATHER_API_KEY != 'your_api_key_here'
    
    # Use mock data if explicitly requested or if no valid API key
    should_use_mock = not USE_REAL_API or not has_valid_api_key
    
    print(f"Generating weather data - Using mock: {should_use_mock}")
    
    if should_use_mock:
        return generate_mock_weather_data()
    else:
        return fetch_real_weather_data()