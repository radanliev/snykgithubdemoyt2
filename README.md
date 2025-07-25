# Snyk GitHub Demo Repository with Weather App

This repository contains a Snyk security scanning demonstration along with a newly added Weather App.

## Components

### 1. Security Demo Apps (Original)
- **app2.py**: Flask application with intentional security vulnerabilities for Snyk testing
- **dummy.py**: Simple hello function
- **requirements.txt**: Contains vulnerable dependencies for security scanning

### 2. Weather App (New) ⛅

A modern, responsive weather application with mock weather data.

#### Features
- 🌤️ Beautiful, responsive UI with gradient background
- 🔍 City search functionality
- 📍 Pre-loaded data for popular cities (London, Paris, New York, Tokyo, Sydney)
- 🎲 Random weather generation for unknown cities
- 📊 Displays temperature, humidity, wind speed, and conditions
- 🕒 Real-time timestamps
- 🔗 REST API endpoints for programmatic access
- 📱 Mobile-friendly responsive design

#### Running the Weather App

```bash
# Start the weather app server
python3 weather_app_simple.py
```

The app will be available at: http://localhost:8000

#### API Usage

Get weather data via API:
```bash
# Get weather for a specific city
curl "http://localhost:8000/api/weather?city=london"

# Response format:
{
  "city": "London",
  "country": "UK",
  "temperature": 15,
  "condition": "Cloudy",
  "humidity": 75,
  "wind_speed": 10,
  "timestamp": "2025-07-25 18:00:00",
  "icon": "☁️"
}
```

#### Supported Cities
The app has pre-configured weather data for:
- London, UK
- Paris, France  
- New York, USA
- Tokyo, Japan
- Sydney, Australia

For other cities, it generates random realistic weather data.

#### Weather Conditions
- ☀️ Sunny
- ☁️ Cloudy
- 🌧️ Rainy
- ⛅ Partly Cloudy
- ❄️ Snowy

### 3. Security Scanning
The repository includes GitHub Actions workflow for Snyk security scanning:
- Scans Python dependencies for vulnerabilities
- Runs on push to main branch and pull requests
- Generates security reports

## File Structure
```
.
├── weather_app_simple.py     # Main weather application
├── app2.py                   # Security demo Flask app
├── dummy.py                  # Simple demo function
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates (if using Flask version)
│   ├── weather_index.html
│   └── weather_result.html
├── .github/
│   └── workflows/
│       └── snyk_scan.yml     # Security scanning workflow
└── README.md                 # This file
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the weather app:
   ```bash
   python3 weather_app_simple.py
   ```

## Development Notes

- The weather app uses only standard Python libraries (no external dependencies)
- Mock data ensures the app works without external API keys
- The app includes both web UI and REST API functionality
- Responsive design works on desktop and mobile devices

## Security Considerations

- The original `app2.py` contains intentional vulnerabilities for security testing
- The weather app follows secure coding practices
- No external API keys or credentials are required
- All inputs are properly escaped to prevent XSS attacks