import requests

def get_external_data(country_name):
    # API 1: Country Data
    country_url = f"https://restcountries.com/v3.1/name/{country_name}"
    c_res = requests.get(country_url)

    if c_res.status_code != 200:
        return None, None, "Country not found"

    # API 2: Weather Data (using Lat/Lng from Country API)
    c_data = c_res.json()[0]
    lat, lon = c_data['latlng']

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    w_res = requests.get(weather_url)

    return c_data, w_res.json() if w_res.status_code == 200 else None, None
def transform_data(country_raw, weather_raw):
    # Requirement III: Modify, Compute, and Clean
    return {
        "country_name": country_raw.get('name', {}).get('common'),
        "capital_city": country_raw.get('capital', ["N/A"])[0],
        "population_count": f"{country_raw.get('population'):,}", # Formatted
        "current_temp_celsius": weather_raw.get('current_weather', {}).get('temperature'),
        "is_warm": weather_raw.get('current_weather', {}).get('temperature', 0) > 20, # Computed field
        "api_version": "v1.0"
    }