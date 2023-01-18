from django.conf import settings
from django.shortcuts import render
import json
import requests


def home(request):
    city_name = _get_city_name(request)
    data_weather = _get_weather_data_from_api(city_name)
    return render(request, 'weather/home.html', {'data': data_weather})


def _get_city_name(request):
    if request.GET.get("city"):
        city_name = request.GET.get("city")
    else:
        city_name = _get_user_city_by_ip()
    return city_name


def _get_user_city_by_ip():
    url = 'http://ip-api.com/json/'

    ip_api = requests.get(url).text
    ip_data = json.loads(ip_api)
    return ip_data['city']


def _get_weather_data_from_api(city):
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
