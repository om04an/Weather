from django.conf import settings
from django.shortcuts import render
import json
import requests


def home(request):
    date_weather = _getting_weather_data_from_api(_ip())
    return render(request, 'weather/home.html', {'date': date_weather})


def _ip():
    url = 'http://ip-api.com/json/'

    ip_api = requests.get(url).text
    date = json.loads(ip_api)
    return date['city']


def _getting_weather_data_from_api(city):
    api_key = settings.API_KEY
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    weather_api = requests.get(url).text
    data = json.loads(weather_api)

    list_info = [f'City --> {data["location"]["name"]}',
                 f'Temperature --> {data["current"]["temp_c"]}',
                 f'Temperature feels-like --> {data["current"]["feelslike_c"]}',
                 f'Precipitation --> {data["current"]["condition"]["text"]}',
                 f'Wind --> {int(data["current"]["wind_kph"] * ( 5 / 18))} m/s',
                 f'Cloudiness --> {data["current"]["cloud"]} %']

    return list_info
