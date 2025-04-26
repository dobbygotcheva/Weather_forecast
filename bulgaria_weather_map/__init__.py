"""
Bulgaria Weather Map - A Flask application for displaying weather information for Bulgarian cities.
"""
from flask import Flask
from bulgaria_weather_map.routes.main import main_bp

def create_app():
    """
    Factory function to create the Flask application.
    This allows for easier testing and debugging.
    
    Returns:
        Flask: The configured Flask application
    """
    # Initialize Flask app with proper configuration
    app = Flask(__name__, 
                static_url_path='/static',
                static_folder='static',
                template_folder='templates')
    
    # Enable debug mode for development
    app.config['DEBUG'] = True
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    # Add CORS headers to allow JavaScript to fetch data
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response
    
    return app