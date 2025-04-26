# Bulgaria Weather Map with OpenLayers

An interactive web map displaying weather information for major cities in Bulgaria using the OpenLayers JavaScript library.

## Description

This project demonstrates how to create an interactive web map that displays weather information for 30 major Bulgarian cities. The application uses OpenLayers for map rendering and Flask as a lightweight backend to serve the web application. Weather data can be fetched from the OpenWeatherMap API or generated as realistic mock data based on seasonal patterns.

## Features

- Interactive map centered on Bulgaria using OpenLayers
- Markers for 30 major Bulgarian cities (including Sofia, Plovdiv, Varna, and many more)
- Weather data from OpenWeatherMap API or realistic mock data generation
- Detailed weather information (temperature, conditions, humidity, wind speed, etc.)
- Popup display when clicking on a city marker
- Responsive design that works on different screen sizes

## Technical Stack

- **Frontend**: OpenLayers (for map rendering), HTML/CSS, JavaScript
- **Backend**: Python with Flask (organized as a proper package)

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install flask requests python-dotenv
   ```
3. Get an API key from OpenWeatherMap (optional, mock data is available):
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Create an API key in your account dashboard
   - Copy the API key
4. Set up your environment variables:
   - Create a `.env` file in the project root (or copy from `.env.example`)
   - Add your OpenWeatherMap API key to the `.env` file:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     USE_REAL_API=true
     ```
5. Run the application:
   ```
   python run.py
   ```
6. Open your browser and navigate to the URL shown in the console (typically `http://127.0.0.1:5000/`)

7. (Optional) Run the tests:
   ```
   python test_app.py
   ```

## Project Structure

```
├── bulgaria_weather_map/       # Main package
│   ├── __init__.py             # Package initialization and app factory
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── config.py           # Configuration settings
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── cities.py           # Bulgarian cities data
│   ├── routes/                 # Route handlers
│   │   ├── __init__.py
│   │   └── main.py             # Main routes
│   ├── static/                 # Static files
│   │   ├── css/
│   │   │   └── style.css       # CSS styles
│   │   ├── icons/              # Weather icons
│   │   ├── js/
│   │   │   └── map.js          # JavaScript for the map
│   │   └── ol/                 # OpenLayers library
│   ├── templates/              # HTML templates
│   │   └── index.html          # Main HTML template
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── openlayers.py       # OpenLayers management
│       ├── server.py           # Server utilities
│       └── weather.py          # Weather data generation
├── run.py                      # Application entry point
├── test_app.py                 # Tests for the application
├── .env                        # Environment variables (API keys)
├── .env.example                # Example environment variables file
└── README.md                   # Project documentation
```

## How It Works

1. The Flask application is organized as a proper package with separate modules for different responsibilities
2. When the application starts, it initializes the Flask app and registers the blueprints
3. When a user visits the site, the main route renders the HTML template with the OpenLayers map
4. JavaScript makes a request to the `/api/weather` endpoint to get weather data
5. The server either fetches real-time data from OpenWeatherMap API or generates realistic mock data
6. OpenLayers loads a base map (OpenStreetMap) and adds custom markers for all Bulgarian cities
7. Clicking a marker displays a popup with detailed weather information for that city

## Key Components

- **Flask Application Factory**: Creates and configures the Flask application
- **Blueprints**: Organize routes into logical groups
- **Configuration Module**: Centralizes application settings
- **Data Models**: Store structured data about Bulgarian cities
- **Utility Functions**: Handle common tasks like OpenLayers management and weather data generation
- **OpenLayers Map**: Provides interactive map functionality in the browser

## Future Improvements

- Add weather forecast for upcoming days
- Implement caching to reduce API calls and improve performance
- Add dynamic weather effects (e.g., rain/snow animations based on current conditions)
- Add a legend and additional map controls
- Implement user location detection to center the map on the user's location
- Add unit tests for all modules
- Implement a database for storing historical weather data

## License

This project is open source and available under the MIT License.
