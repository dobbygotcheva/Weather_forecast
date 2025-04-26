"""
Main routes for the Bulgaria Weather Map application.
"""
from flask import render_template, jsonify, Blueprint
from bulgaria_weather_map.utils.openlayers import ensure_openlayers_available
from bulgaria_weather_map.utils.weather import get_weather_data
from bulgaria_weather_map.models.cities import CITIES

# Create a Blueprint for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main page of the application."""
    print("Rendering index page")
    # Make sure OpenLayers is downloaded
    from flask import current_app
    ensure_openlayers_available(current_app.static_folder)
    return render_template('index.html')

@main_bp.route('/debug')
def debug():
    """Debug route to help troubleshoot issues."""
    from flask import current_app
    from bulgaria_weather_map.utils.openlayers import check_openlayers_available
    from bulgaria_weather_map.config.config import OPENWEATHER_API_KEY, USE_REAL_API

    debug_info = {
        "app_running": True,
        "routes": [str(rule) for rule in current_app.url_map.iter_rules()],
        "static_folder": current_app.static_folder,
        "template_folder": current_app.template_folder,
        "environment_vars": {
            "USE_REAL_API": USE_REAL_API,
            "API_KEY_SET": OPENWEATHER_API_KEY != 'your_api_key_here',
            "DEBUG": current_app.debug
        },
        "cities_count": len(CITIES),
        "openlayers_available": check_openlayers_available(current_app.static_folder)
    }
    return jsonify(debug_info)

@main_bp.route('/api/test')
def test_api():
    """Test route to verify API functionality."""
    return jsonify({"status": "API is working", "message": "If you see this, the API is functional"})

@main_bp.route('/api/weather')
def get_weather():
    """API endpoint to get weather data for Bulgarian cities."""
    print("Weather API endpoint called")

    try:
        # Get weather data (either mock or real)
        weather_data = get_weather_data()

        # Return the weather data
        return jsonify(weather_data)

    except Exception as e:
        print(f"ERROR in get_weather route: {str(e)}")
        # Return a minimal response even in case of error
        error_response = {
            "error": str(e),
            "fallback_data": {
                'Sofia': {
                    'coordinates': [float(CITIES['Sofia']['lon']), float(CITIES['Sofia']['lat'])],
                    'temperature': "N/A (Error)",
                    'condition': "Unknown"
                }
            }
        }
        return jsonify(error_response)
