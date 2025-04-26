"""
Utility functions for managing OpenLayers resources.
"""
import requests
from pathlib import Path
import os

def check_openlayers_available(static_folder):
    """
    Check if OpenLayers files are available locally.
    
    Args:
        static_folder (str): Path to the static folder
        
    Returns:
        bool: True if OpenLayers files exist, False otherwise
    """
    ol_js_path = Path(static_folder) / 'ol' / 'ol.js'
    ol_css_path = Path(static_folder) / 'ol' / 'ol.css'
    return ol_js_path.exists() and ol_css_path.exists()

def ensure_openlayers_available(static_folder):
    """
    Ensure OpenLayers files are available locally.
    Downloads them if they don't exist.
    
    Args:
        static_folder (str): Path to the static folder
        
    Returns:
        bool: True if OpenLayers files are available, False otherwise
    """
    if check_openlayers_available(static_folder):
        print("OpenLayers files already available")
        return True

    print("Downloading OpenLayers files...")
    try:
        # Create the ol directory if it doesn't exist
        ol_dir = Path(static_folder) / 'ol'
        ol_dir.mkdir(exist_ok=True)

        # Download OpenLayers JavaScript
        js_url = "https://cdn.jsdelivr.net/npm/ol@v7.4.0/dist/ol.js"
        js_response = requests.get(js_url)
        if js_response.status_code == 200:
            with open(ol_dir / 'ol.js', 'wb') as f:
                f.write(js_response.content)
            print("Downloaded ol.js successfully")
        else:
            print(f"Failed to download ol.js: {js_response.status_code}")

        # Download OpenLayers CSS
        css_url = "https://cdn.jsdelivr.net/npm/ol@v7.4.0/dist/ol.css"
        css_response = requests.get(css_url)
        if css_response.status_code == 200:
            with open(ol_dir / 'ol.css', 'wb') as f:
                f.write(css_response.content)
            print("Downloaded ol.css successfully")
        else:
            print(f"Failed to download ol.css: {css_response.status_code}")

        return check_openlayers_available(static_folder)
    except Exception as e:
        print(f"Error downloading OpenLayers: {str(e)}")
        return False