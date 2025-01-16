import requests
import os
from dotenv import load_dotenv
load_dotenv()
def get_temp_hum(district, state=None, month=None):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise Exception("API key not found. Please set it in the .env file.")
    # First, try fetching data using district
    district_url = f"https://api.openweathermap.org/data/2.5/weather?q={district}&appid={api_key}"
    district_response = requests.get(district_url)

    # If the request using district fails, try using state
    if district_response.status_code != 200:
        if state is not None:
            state_url = f"https://api.openweathermap.org/data/2.5/weather?q={state}&appid={api_key}"
            state_response = requests.get(state_url)

            if state_response.status_code != 200:
                print(f"Failed to fetch data for both {district} and {state}")
                raise Exception(f"Unable to get the temperature for {district} or {state}")

            data = state_response.json()
        else:
            print(f"Failed to fetch data for {district}")
            raise Exception(f"Unable to get the temperature for {district}")
    else:
        data = district_response.json()

    humidity = data['main']['humidity']
    temp = (data['main']['temp_min'] + data['main']['temp_max']) / 2 - 273.15
    return temp, humidity
