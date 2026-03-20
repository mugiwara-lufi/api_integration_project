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