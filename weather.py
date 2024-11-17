#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta
import argparse
import pytz

def format_weather_output(dt, temp_k, rain, wind_speed, clouds, timezone, is_current=False):
    local_tz = pytz.timezone(timezone)
    dt_local = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    formatted_dt = dt_local.strftime('%-m/%-d %-I%p')
    temp_f = (temp_k - 273.15) * 9/5 + 32
    output = f"{formatted_dt:<10} | Temp: {temp_f:>6.2f}F | Rain: {rain:>5}mm | Wind: {wind_speed:>5}m/s | Clouds: {clouds:>3}%"
    if is_current:
        return f"\033[92m{output}\033[0m"  # Green color for the first entry
    return output

def fetch_weather(api_key, lat, lon, hours, timezone):
    # Construct the API URLs
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    # Call the current weather API and parse the result
    current_response = requests.get(current_weather_url)
    current_data = current_response.json()

    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Format the current weather data
    current_dt = datetime.fromtimestamp(current_data['dt'], pytz.utc)
    current_temp_k = current_data['main']['temp']
    current_rain = current_data.get('rain', {}).get('1h', 0)
    current_wind_speed = current_data['wind']['speed']
    current_clouds = current_data['clouds']['all']
    current_output = format_weather_output(current_dt, current_temp_k, current_rain, current_wind_speed, current_clouds, timezone, is_current=True)

    # Print the current weather data as the first entry
    print(current_output)

    # Call the forecast API and parse the results
    response = requests.get(forecast_url)
    data = response.json()

    # Print the results for the specified number of hours
    local_tz = pytz.timezone(timezone)
    now_local = now_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
    for item in data['list']:
        dt_txt = item['dt_txt']
        dt_utc = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
        dt_local = dt_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
        if dt_local <= now_local + timedelta(hours=hours):
            temp_k = item['main']['temp']
            rain = item.get('rain', {}).get('3h', 0)
            wind_speed = item['wind']['speed']
            clouds = item['clouds']['all']
            output = format_weather_output(dt_utc, temp_k, rain, wind_speed, clouds, timezone)
            print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather forecast data.")
    parser.add_argument('--api_key', type=str, default=os.getenv('OPEN_WEATHER_MAP_API_KEY'), help='OpenWeatherMap API key')
    parser.add_argument('--lat', type=str, default=os.getenv('WEATHER_LAT'), help='Latitude for the weather forecast')
    parser.add_argument('--lon', type=str, default=os.getenv('WEATHER_LON'), help='Longitude for the weather forecast')
    parser.add_argument('--hours', type=int, default=24, help='Number of hours to fetch the forecast for')
    parser.add_argument('--timezone', type=str, default='US/Pacific', help='Timezone for the weather forecast')

    args = parser.parse_args()

    fetch_weather(args.api_key, args.lat, args.lon, args.hours, args.timezone)