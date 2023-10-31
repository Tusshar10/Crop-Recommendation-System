import requests

def get_temp_hum(district, state=None, month=None):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={district}&appid=af1253e5ac93e4757ad434376e322761"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Unable to get the temperature for {district}")

    data = response.json()
    humidity = data['main']['humidity']
    temp = (data['main']['temp_min']+data['main']['temp_max'])/2-273.15
    return (temp, humidity)
