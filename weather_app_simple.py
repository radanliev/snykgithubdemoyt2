#!/usr/bin/env python3
"""
Simple Weather App - Mock Version
A basic weather application that provides mock weather data for demonstration purposes.
No external dependencies required beyond basic Python.
"""

import json
import random
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import html

# Mock weather data for demonstration
CITIES_WEATHER = {
    'london': {
        'city': 'London',
        'country': 'UK',
        'temperature': 15,
        'condition': 'Cloudy',
        'humidity': 75,
        'wind_speed': 10
    },
    'paris': {
        'city': 'Paris',
        'country': 'France',
        'temperature': 18,
        'condition': 'Sunny',
        'humidity': 60,
        'wind_speed': 8
    },
    'new york': {
        'city': 'New York',
        'country': 'USA',
        'temperature': 22,
        'condition': 'Partly Cloudy',
        'humidity': 65,
        'wind_speed': 12
    },
    'tokyo': {
        'city': 'Tokyo',
        'country': 'Japan',
        'temperature': 25,
        'condition': 'Rainy',
        'humidity': 80,
        'wind_speed': 6
    },
    'sydney': {
        'city': 'Sydney',
        'country': 'Australia',
        'temperature': 20,
        'condition': 'Sunny',
        'humidity': 55,
        'wind_speed': 15
    }
}

def get_random_weather_variation():
    """Add some random variation to make weather data more dynamic"""
    return random.randint(-3, 3)

def get_weather_icon(condition):
    """Return appropriate emoji for weather condition"""
    icons = {
        'Sunny': '☀️',
        'Cloudy': '☁️',
        'Rainy': '🌧️',
        'Partly Cloudy': '⛅',
        'Snowy': '❄️'
    }
    return icons.get(condition, '🌤️')

def get_weather_data(city):
    """Get weather data for a city"""
    city_lower = city.lower().strip()
    
    if city_lower in CITIES_WEATHER:
        weather_data = CITIES_WEATHER[city_lower].copy()
        # Add some random variation
        weather_data['temperature'] += get_random_weather_variation()
    else:
        # Generate random weather for unknown cities
        conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Snowy']
        weather_data = {
            'city': city.title(),
            'country': 'Unknown',
            'temperature': random.randint(-10, 35),
            'condition': random.choice(conditions),
            'humidity': random.randint(30, 90),
            'wind_speed': random.randint(0, 25)
        }
    
    weather_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_data['icon'] = get_weather_icon(weather_data['condition'])
    return weather_data

def generate_html_page(weather_data=None, error=None):
    """Generate HTML page for weather display"""
    style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h1 { color: #2d3436; margin-bottom: 30px; font-size: 2.5em; }
        .weather-icon { font-size: 4em; margin-bottom: 20px; }
        .search-form { margin-bottom: 30px; }
        input[type="text"] {
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 25px;
            width: 60%;
            font-size: 16px;
            margin-right: 10px;
            outline: none;
        }
        input[type="text"]:focus { border-color: #74b9ff; }
        button {
            padding: 15px 25px;
            background: #74b9ff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #0984e3; }
        .error { color: #e74c3c; margin-top: 20px; font-weight: bold; }
        .weather-result {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .temperature { font-size: 3em; color: #e17055; font-weight: bold; }
        .condition { font-size: 1.5em; color: #2d3436; margin: 10px 0; }
        .details { display: flex; justify-content: space-around; margin-top: 20px; }
        .detail-item { text-align: center; }
        .detail-value { font-size: 1.2em; font-weight: bold; }
        .detail-label { color: #636e72; font-size: 0.9em; }
        .city-link {
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #f8f9fa;
            color: #2d3436;
            text-decoration: none;
            border-radius: 20px;
        }
        .city-link:hover { background: #e9ecef; }
        .timestamp { color: #636e72; font-size: 0.9em; margin-top: 15px; }
    </style>
    """
    
    if weather_data:
        content = f"""
        <div class="weather-icon">{weather_data['icon']}</div>
        <h1>Weather in {html.escape(weather_data['city'])}</h1>
        <div class="weather-result">
            <div class="temperature">{weather_data['temperature']}°C</div>
            <div class="condition">{html.escape(weather_data['condition'])}</div>
            <div class="details">
                <div class="detail-item">
                    <div class="detail-value">{weather_data['humidity']}%</div>
                    <div class="detail-label">Humidity</div>
                </div>
                <div class="detail-item">
                    <div class="detail-value">{weather_data['wind_speed']}</div>
                    <div class="detail-label">Wind (km/h)</div>
                </div>
            </div>
            <div class="timestamp">Last updated: {weather_data['timestamp']}</div>
        </div>
        <form class="search-form" action="/weather" method="GET">
            <input type="text" name="city" placeholder="Search another city..." required>
            <button type="submit">Search</button>
        </form>
        <a href="/" style="color: #74b9ff; text-decoration: none;">← Back to Home</a>
        """
    else:
        content = f"""
        <div class="weather-icon">🌤️</div>
        <h1>Weather App</h1>
        <form class="search-form" action="/weather" method="GET">
            <input type="text" name="city" placeholder="Enter city name..." required>
            <button type="submit">Get Weather</button>
        </form>
        {'<div class="error">' + html.escape(error) + '</div>' if error else ''}
        <div style="margin-top: 30px;">
            <h3>Popular Cities:</h3>
            <a href="/weather?city=london" class="city-link">London</a>
            <a href="/weather?city=paris" class="city-link">Paris</a>
            <a href="/weather?city=new york" class="city-link">New York</a>
            <a href="/weather?city=tokyo" class="city-link">Tokyo</a>
            <a href="/weather?city=sydney" class="city-link">Sydney</a>
        </div>
        <div style="margin-top: 30px; color: #636e72; font-size: 14px;">
            <p>🔗 API Access: <code>/api/weather?city=cityname</code></p>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather App</title>
        {style}
    </head>
    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        if path == '/':
            # Home page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(generate_html_page().encode())
            
        elif path == '/weather':
            # Weather page
            city = query_params.get('city', [''])[0]
            if city:
                weather_data = get_weather_data(city)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(generate_html_page(weather_data=weather_data).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(generate_html_page(error="Please enter a city name").encode())
                
        elif path == '/api/weather':
            # API endpoint
            city = query_params.get('city', [''])[0]
            if city:
                weather_data = get_weather_data(city)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(weather_data, indent=2).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {'error': 'City parameter is required'}
                self.wfile.write(json.dumps(error_response).encode())
                
        else:
            # 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1><a href="/">Go to Weather App</a>')

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(port=8000):
    """Run the weather app server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, WeatherHandler)
    print(f"Weather App starting on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()