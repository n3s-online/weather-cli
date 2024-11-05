# weather-cli
A weather script that I can call via my CLI.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/weather-cli.git
    cd weather-cli
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a symbolic link to the script in your `/usr/local/bin` directory (or another directory in your `$PATH`):
    ```bash
    ln -s /path/to/weather.py /usr/local/bin/weather
    ```

## Configuration
Set the following environment variables in your shell profile (e.g., `.bashrc`, `.zshrc`) to set defaults for the CLI:
- `OPEN_WEATHER_MAP_API_KEY`: Your OpenWeatherMap API key.
- `WEATHER_LAT`: Default latitude for the weather forecast.
- `WEATHER_LON`: Default longitude for the weather forecast.

## Usage
To get the weather forecast, run the script with the following arguments:
- `--api_key`: OpenWeatherMap API key (optional, defaults to environments `OPEN_WEATHER_MAP_API_KEY`).
- `--lat`: Latitude for the weather forecast (optional, defaults to environments `WEATHER_LAT`).
- `--lon`: Longitude for the weather forecast (optional, defaults to environments `WEATHER_LON`).
- `--hours`: Number of hours for the weather forecast (optional, defaults to 24).
- `--timezone`: Timezone for the weather forecast (optional, defaults to local).

Example:
```bash
# Get the weather forecast for your current location for 24 hours
weather

# Get the wetaher forecast for 12 hours for a specific locationusing New York's timezone
weather --api_key your_api_key --lat 40.7128 --lon -74.0060 --hours 12 --timezone America/New_York
```