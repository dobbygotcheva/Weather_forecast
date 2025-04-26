"""
Entry point for running the Bulgaria Weather Map application.
"""
from bulgaria_weather_map import create_app
from bulgaria_weather_map.utils.server import find_available_port
from bulgaria_weather_map.config.config import OPENWEATHER_API_KEY, USE_REAL_API

def main():
    """
    Main function to run the application.
    """
    # Create the Flask application
    app = create_app()
    
    # Print debug information
    print("Starting Flask application...")

    api_key_status = 'Set' if OPENWEATHER_API_KEY != 'your_api_key_here' else 'Not Set (will use mock data)'
    print(f"OpenWeatherMap API Key: {api_key_status}")

    using_mock = not USE_REAL_API or OPENWEATHER_API_KEY == 'your_api_key_here'
    mock_status = "Yes (either by configuration or missing API key)" if using_mock else "No"

    print(f"Using mock data: {mock_status}")

    if using_mock:
        print("Note: Using mock weather data. To use real data, set a valid OPENWEATHER_API_KEY in your environment variables.")

    # Find an available port and run the application
    try:
        port = find_available_port()
        print(f"Starting server on port {port}")
        app.run(debug=True, port=port)
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    main()