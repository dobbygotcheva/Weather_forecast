// Bulgaria Weather Map - Main JavaScript
// Global variables
let map = null;
let vectorSource = null;
let mapInitialized = false;

// Constants for display
// Weather condition colors - used for the circle markers on the map
// These colors match the ones used in the weather legend in the sidebar
const WEATHER_COLORS = {
    'Clear': '#f39c12',      // Orange/yellow for clear/sunny
    'Clouds': '#7f8c8d',     // Gray for cloudy
    'Rain': '#3498db',       // Blue for rain
    'Snow': '#74b9ff',       // Light blue for snow
    'Mist': '#95a5a6',       // Light gray for mist/fog
    'Thunderstorm': '#f1c40f', // Yellow for thunderstorms
    'Unknown': '#95a5a6'     // Default gray for unknown conditions
};

// Weather icons - FontAwesome icon names for each weather condition
// These are used in popups and the simple map fallback
const WEATHER_ICONS = {
    'Clear': 'sun',
    'Clouds': 'cloud',
    'Rain': 'cloud-rain',
    'Snow': 'snowflake',
    'Mist': 'smog',
    'Thunderstorm': 'bolt',
    'Unknown': 'question-circle'
};

// Weather icon filenames - mapping between weather conditions and PNG icon files
// These are used for the map markers
const WEATHER_ICON_FILES = {
    'Clear': 'clear.png',
    'Clouds': 'clouds.png',
    'Rain': 'rain.png',
    'Snow': 'snowy.png',
    'Mist': 'mist.png',
    'Thunderstorm': 'storm.png',
    'Unknown': 'clouds.png'  // Fallback icon
};

// FontAwesome icon codes for direct use in text
// Note: These were previously used to embed icons directly in OpenLayers text
// but this approach has been replaced with a simpler solution using colored circles
// These are kept for reference or future use
const ICON_CODES = {
    'sun': '185',           // fa-sun
    'cloud': '0c2',         // fa-cloud
    'cloud-rain': '73c',    // fa-cloud-rain
    'snowflake': 'f2c',     // fa-snowflake
    'smog': 'f75',          // fa-smog
    'bolt': '0e7',          // fa-bolt
    'question-circle': '059' // fa-question-circle
};

// Helper function to get FontAwesome icon code
// Note: This function is not currently being used in the code
// It was previously used for embedding icons in OpenLayers text
// Kept for reference or future use
function getIconCode(iconName) {
    return ICON_CODES[iconName] || ICON_CODES['question-circle'];
}

// Fallback data if API fails
const FALLBACK_DATA = {
    'Sofia': {
        coordinates: [23.3219, 42.6977],
        temperature: '20.0°C',
        condition: 'Clear',
        humidity: '45%',
        wind_speed: '3.2 m/s',
        pressure: '1015 hPa',
        feels_like: '19.5°C',
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
    },
    'Plovdiv': {
        coordinates: [24.7453, 42.1354],
        temperature: '18.2°C',
        condition: 'Clouds',
        humidity: '60%',
        wind_speed: '2.8 m/s',
        pressure: '1012 hPa',
        feels_like: '17.5°C',
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
    },
    'Varna': {
        coordinates: [27.9147, 43.2141],
        temperature: '22.3°C',
        condition: 'Rain',
        humidity: '75%',
        wind_speed: '5.1 m/s',
        pressure: '1008 hPa',
        feels_like: '21.8°C',
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
    },
    'Burgas': {
        coordinates: [27.4626, 42.5048],
        temperature: '21.5°C',
        condition: 'Clear',
        humidity: '55%',
        wind_speed: '4.2 m/s',
        pressure: '1010 hPa',
        feels_like: '20.9°C',
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
    },
    'Ruse': {
        coordinates: [25.9714, 43.8564],
        temperature: '19°C',
        condition: 'Clouds'
    },
    'Stara Zagora': {
        coordinates: [25.6257, 42.4280],
        temperature: '21°C',
        condition: 'Clear'
    },
    'Pleven': {
        coordinates: [24.6180, 43.4170],
        temperature: '18°C',
        condition: 'Clouds'
    },
    'Sliven': {
        coordinates: [26.3220, 42.6816],
        temperature: '20°C',
        condition: 'Clear'
    },
    'Dobrich': {
        coordinates: [27.8333, 43.5667],
        temperature: '19°C',
        condition: 'Rain'
    },
    'Shumen': {
        coordinates: [26.9361, 43.2714],
        temperature: '18°C',
        condition: 'Clouds'
    },
    'Pernik': {
        coordinates: [23.0333, 42.6000],
        temperature: '17°C',
        condition: 'Clear'
    },
    'Haskovo': {
        coordinates: [25.5556, 41.9333],
        temperature: '22°C',
        condition: 'Clear'
    },
    'Yambol': {
        coordinates: [26.5000, 42.4833],
        temperature: '21°C',
        condition: 'Clouds'
    },
    'Pazardzhik': {
        coordinates: [24.3333, 42.2000],
        temperature: '19°C',
        condition: 'Clear'
    },
    'Blagoevgrad': {
        coordinates: [23.1000, 42.0167],
        temperature: '18°C',
        condition: 'Clouds'
    },
    'Veliko Tarnovo': {
        coordinates: [25.6278, 43.0757],
        temperature: '19°C',
        condition: 'Clear'
    },
    'Vidin': {
        coordinates: [22.8667, 43.9833],
        temperature: '17°C',
        condition: 'Rain'
    },
    'Gabrovo': {
        coordinates: [25.3167, 42.8667],
        temperature: '16°C',
        condition: 'Clouds'
    },
    'Asenovgrad': {
        coordinates: [24.8667, 42.0167],
        temperature: '20°C',
        condition: 'Clear'
    },
    'Kazanlak': {
        coordinates: [25.4000, 42.6167],
        temperature: '19°C',
        condition: 'Clouds'
    },
    'Kardzhali': {
        coordinates: [25.3667, 41.6500],
        temperature: '21°C',
        condition: 'Clear'
    },
    'Montana': {
        coordinates: [23.2250, 43.4125],
        temperature: '18°C',
        condition: 'Clouds'
    },
    'Dimitrovgrad': {
        coordinates: [25.5833, 42.0500],
        temperature: '20°C',
        condition: 'Clear'
    },
    'Lovech': {
        coordinates: [24.7167, 43.1333],
        temperature: '19°C',
        condition: 'Clouds'
    },
    'Silistra': {
        coordinates: [27.2667, 44.1167],
        temperature: '18°C',
        condition: 'Rain'
    },
    'Targovishte': {
        coordinates: [26.5833, 43.2500],
        temperature: '19°C',
        condition: 'Clouds'
    },
    'Razgrad': {
        coordinates: [26.5167, 43.5333],
        temperature: '18°C',
        condition: 'Clear'
    },
    'Smolyan': {
        coordinates: [24.6931, 41.5775],
        temperature: '15°C',
        condition: 'Clouds'
    },
    'Kyustendil': {
        coordinates: [22.6833, 42.2833],
        temperature: '17°C',
        condition: 'Clear'
    }
};

// Debug utility functions
function debugMsg(msg) {
    console.log(msg);
    const debugContent = document.getElementById('debug-content');
    if (debugContent) {
        debugContent.innerHTML += `<p>${msg}</p>`;
    }
}

function showError(error) {
    console.error(error);
    const debugOutput = document.getElementById('debug-output');
    if (debugOutput) {
        debugOutput.style.display = 'block';
        const debugContent = document.getElementById('debug-content');
        if (debugContent) {
            debugContent.innerHTML += `<p style="color: red">Error: ${error}</p>`;
        }
    }
}

// Update status display
function updateStatus(message) {
    const statusElement = document.querySelector('.weather-status');
    if (statusElement) {
        statusElement.innerHTML = `<p><i class="fas fa-info-circle"></i> ${message}</p>`;
    }
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    debugMsg("Page loaded, initializing map...");

    // Initialize everything
    initializeApp();
});

// Main application initialization
function initializeApp() {
    // Check if map container exists
    const mapElement = document.getElementById('map');
    if (!mapElement) {
        showError('Map container not found in the document');
        return;
    }

    // First try to initialize with OpenLayers
    if (typeof ol !== 'undefined') {
        try {
            initializeOpenLayersMap();
        } catch (error) {
            showError('Error initializing OpenLayers map: ' + error.message);
            createSimpleMap();
        }
    } else {
        showError('OpenLayers library not available');
        createSimpleMap();
    }

    // Set up refresh button
    const refreshButton = document.getElementById('refresh-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';

            fetchWeatherData();

            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Now';
            }, 2000);
        });
    }

    // Auto-refresh every 5 minutes
    setInterval(fetchWeatherData, 300000);
}

// Create an OpenLayers map
function initializeOpenLayersMap() {
    debugMsg("Initializing OpenLayers map...");

    // Create a vector source for markers
    vectorSource = new ol.source.Vector();

    // Create vector layer
    const vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });

    // Create the map
    map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            vectorLayer
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([25.4858, 42.7339]), // Center of Bulgaria
            zoom: 7,
            minZoom: 6,
            maxZoom: 10
        })
    });

    // Create a popup overlay for displaying weather information
    const popupElement = document.createElement('div');
    popupElement.className = 'ol-popup';
    popupElement.style.display = 'none';

    const popup = new ol.Overlay({
        element: popupElement,
        positioning: 'bottom-center',
        stopEvent: false,
        offset: [0, -10]
    });

    map.addOverlay(popup);

    // Handle click events on the map
    map.on('click', function(evt) {
        // Hide existing popup
        popupElement.style.display = 'none';

        // Check if a feature was clicked
        const feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
            return feature;
        });

        if (feature) {
            // Get feature properties
            const cityName = feature.get('name');
            const temperature = feature.get('temperature');
            const condition = feature.get('condition');
            const humidity = feature.get('humidity') || 'N/A';
            const windSpeed = feature.get('wind_speed') || 'N/A';
            const pressure = feature.get('pressure') || 'N/A';
            const feelsLike = feature.get('feels_like') || 'N/A';
            const timestamp = feature.get('timestamp') || 'N/A';

            // Show popup with more detailed weather information
            const iconFile = WEATHER_ICON_FILES[condition] || WEATHER_ICON_FILES['Unknown'];
            popupElement.innerHTML = `
                <div class="popup-content">
                    <h3>${cityName}</h3>
                    <p><img src="/static/icons/${iconFile}" style="width: 16px; height: 16px; vertical-align: middle;"> ${condition}</p>
                    <p><i class="fas fa-temperature-high"></i> Temperature: ${temperature}</p>
                    <p><i class="fas fa-temperature-low"></i> Feels like: ${feelsLike}</p>
                    <p><i class="fas fa-tint"></i> Humidity: ${humidity}</p>
                    <p><i class="fas fa-wind"></i> Wind: ${windSpeed}</p>
                    <p><i class="fas fa-compress-alt"></i> Pressure: ${pressure}</p>
                    <p><i class="fas fa-clock"></i> Updated: ${timestamp}</p>
                </div>
            `;

            popup.setPosition(evt.coordinate);
            popupElement.style.display = 'block';
        }
    });

    // Change cursor when hovering over a feature
    map.on('pointermove', function(e) {
        const hit = map.hasFeatureAtPixel(e.pixel);
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

    // Successfully initialized
    mapInitialized = true;
    debugMsg("OpenLayers map initialized successfully");

    // Fetch weather data
    fetchWeatherData();
}

// Create a simplified fallback map
function createSimpleMap() {
    debugMsg("Creating simple fallback map");

    const mapElement = document.getElementById('map');
    mapElement.innerHTML = '';

    // Simple map container
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.backgroundColor = '#e0f3f8';
    container.style.position = 'relative';

    // Map image
    const image = document.createElement('img');
    image.src = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Bulgaria_%28orthographic_projection%29.svg';
    image.alt = 'Map of Bulgaria';
    image.style.width = '80%';
    image.style.maxHeight = '80%';
    image.style.margin = '30px auto';
    image.style.display = 'block';

    container.appendChild(image);
    mapElement.appendChild(container);

    // Add markers to the simple map
    displaySimpleMarkers(container, FALLBACK_DATA);

    // Update status
    updateStatus('Using simplified map (OpenLayers unavailable)');
}

// Display markers on the simple map
function displaySimpleMarkers(container, data) {
    // Approximate positions for cities on the image
    const positions = {
        'Sofia': { left: '38%', top: '55%' },
        'Plovdiv': { left: '50%', top: '60%' },
        'Varna': { left: '70%', top: '32%' },
        'Burgas': { left: '72%', top: '45%' },
        'Ruse': { left: '58%', top: '25%' },
        'Stara Zagora': { left: '55%', top: '52%' }
    };

    // Create a marker for each city
    for (const [city, cityData] of Object.entries(data)) {
        // Skip if we don't have a position for this city
        if (!positions[city]) continue;

        const position = positions[city];
        const condition = cityData.condition || 'Unknown';
        const color = WEATHER_COLORS[condition] || WEATHER_COLORS['Unknown'];

        // Marker container
        const marker = document.createElement('div');
        marker.style.position = 'absolute';
        marker.style.left = position.left;
        marker.style.top = position.top;
        marker.style.transform = 'translate(-50%, -50%)';
        marker.style.zIndex = '100';
        marker.style.cursor = 'pointer';

        // City dot
        const dot = document.createElement('div');
        dot.style.width = '12px';
        dot.style.height = '12px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = color;
        dot.style.border = '2px solid white';
        dot.style.boxShadow = '0 0 4px rgba(0,0,0,0.5)';

        // City name and weather info
        const label = document.createElement('div');
        const icon = WEATHER_ICONS[condition] || WEATHER_ICONS['Unknown'];
        const temp = cityData.temperature || 'N/A';

        // Create city name text
        const cityText = document.createElement('div');
        cityText.textContent = city;
        cityText.style.textAlign = 'center';
        cityText.style.fontWeight = 'bold';

        // Create weather icon and temperature
        const weatherInfo = document.createElement('div');

        // Use PNG weather icon instead of FontAwesome
        const iconFile = WEATHER_ICON_FILES[condition] || WEATHER_ICON_FILES['Unknown'];
        weatherInfo.innerHTML = `<img src="/static/icons/${iconFile}" style="width: 16px; height: 16px; vertical-align: middle;"> ${temp}`;
        weatherInfo.style.textAlign = 'center';
        weatherInfo.style.marginTop = '3px';

        // Add both to label
        label.appendChild(cityText);
        label.appendChild(weatherInfo);

        label.style.position = 'absolute';
        label.style.top = '-35px';
        label.style.left = '50%';
        label.style.transform = 'translateX(-50%)';
        label.style.whiteSpace = 'nowrap';
        label.style.fontSize = '12px';
        label.style.textShadow = '1px 1px 1px white';
        label.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        label.style.padding = '2px 5px';
        label.style.borderRadius = '3px';

        marker.appendChild(dot);
        marker.appendChild(label);

        // Add click handler to show info
        marker.addEventListener('click', function() {
            alert(`${city}\nTemperature: ${cityData.temperature}\nCondition: ${condition}`);
        });

        container.appendChild(marker);
    }
}

// Fetch weather data from the server
function fetchWeatherData() {
    debugMsg("Fetching weather data...");
    updateStatus('Fetching weather data...');

    fetch('/api/weather')
        .then(response => {
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            debugMsg("Weather data received");

            if (typeof data !== 'object' || Object.keys(data).length === 0) {
                throw new Error("Empty data received");
            }

            // Display the weather data on the map
            displayWeatherData(data);
        })
        .catch(error => {
            showError(`Failed to load weather data: ${error.message}`);

            // Use fallback data
            displayWeatherData(FALLBACK_DATA);
        });
}

// Display weather data on the map
function displayWeatherData(data) {
    if (mapInitialized && map && vectorSource) {
        // Display on OpenLayers map
        displayOpenLayersMarkers(data);
    } else {
        // Display on simple map
        const mapElement = document.getElementById('map');
        if (mapElement.firstChild) {
            mapElement.innerHTML = '';
        }
        createSimpleMap();
    }

    // Update status
    const now = new Date();
    updateStatus(`Weather data updated at ${now.toLocaleTimeString()}`);
}

// Display markers on the OpenLayers map
function displayOpenLayersMarkers(data) {
    // Clear existing markers
    vectorSource.clear();

    // Add markers for each city
    for (const [city, cityData] of Object.entries(data)) {
        try {
            if (!cityData.coordinates || cityData.coordinates.length !== 2) {
                console.warn(`Invalid coordinates for ${city}`);
                continue;
            }

            // Parse coordinates as numbers
            const lon = parseFloat(cityData.coordinates[0]);
            const lat = parseFloat(cityData.coordinates[1]);

            if (isNaN(lon) || isNaN(lat)) {
                console.warn(`Invalid coordinate values for ${city}`);
                continue;
            }

            // Create marker feature with all weather properties
            const feature = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
                name: city,
                temperature: cityData.temperature,
                condition: cityData.condition || 'Unknown',
                humidity: cityData.humidity,
                wind_speed: cityData.wind_speed,
                pressure: cityData.pressure,
                feels_like: cityData.feels_like,
                timestamp: cityData.timestamp
            });

            // Style the marker
            const condition = cityData.condition || 'Unknown';
            const color = WEATHER_COLORS[condition] || WEATHER_COLORS['Unknown'];
            const icon = WEATHER_ICONS[condition] || WEATHER_ICONS['Unknown'];
            const temp = cityData.temperature || 'N/A';

            // Create text with city name and temperature (without trying to use FontAwesome icons directly)
            const iconText = `${city}\n${temp}`;

            // Create a style with a weather icon for the weather condition
            const iconFile = WEATHER_ICON_FILES[condition] || WEATHER_ICON_FILES['Unknown'];
            const iconSrc = `/static/icons/${iconFile}`;

            const style = new ol.style.Style({
                image: new ol.style.Icon({
                    src: iconSrc,
                    scale: 0.1,  // Reduced from 0.3 to make icons much much smaller
                    anchor: [0.5, 0.5]
                }),
                text: new ol.style.Text({
                    text: iconText,
                    font: '12px Arial',
                    offsetY: -20,
                    textAlign: 'center',
                    textBaseline: 'bottom',
                    fill: new ol.style.Fill({
                        color: '#000'
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#fff',
                        width: 3
                    })
                })
            });

            feature.setStyle(style);
            vectorSource.addFeature(feature);

            debugMsg(`Added marker for ${city}`);
        } catch (error) {
            console.error(`Error adding marker for ${city}:`, error);
        }
    }
}
