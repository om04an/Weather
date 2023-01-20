from django.conf import settings
from django.shortcuts import render
from .serializers import WeatherSerializer
from .models import City
import json
import requests


def home(request):
    data_weather = json.loads(combined_api(request))
    return render(request, 'weather/home.html', {'data': data_weather.values})


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

    list_info = [data["location"]["name"],
                 int(data["current"]["temp_c"]),
                 int(data["current"]["feelslike_c"]),
                 data["current"]["condition"]["text"],
                 int(data["current"]["wind_kph"] * (5 / 18)),
                 data["current"]["cloud"]
                 ]
    return list_info


def _edit_data_db(all_data_weather):
    post = City.objects.get(city=all_data_weather[0])
    post.temperature = all_data_weather[1]
    post.temperature_feelslike = all_data_weather[2]
    post.precipitation = all_data_weather[3]
    post.wind = all_data_weather[4]
    post.cloudiness = all_data_weather[5]
    post.save()


def _create_data_db(all_data_weather):
    City.objects.create(city=all_data_weather[0],
                        temperature=all_data_weather[1],
                        temperature_feelslike=all_data_weather[2],
                        precipitation=all_data_weather[3],
                        wind=all_data_weather[4],
                        cloudiness=all_data_weather[5]
                        )


def _update_or_create_data_db(request):
    city = _get_city_name(request)
    all_data_weather = _get_weather_data_from_api(city)
    data_weather = City.objects.filter(city=all_data_weather[0])

    if data_weather:
        _edit_data_db(all_data_weather)
    else:
        _create_data_db(all_data_weather)


def combined_api(request):
    _update_or_create_data_db(request)
    city = _get_city_name(request)
    all_data_weather = _get_weather_data_from_api(city)

    data_weather = City.objects.filter(city=all_data_weather[0])

    serializer = WeatherSerializer(data_weather, many=True)
    data = json.dumps([dict(i) for i in serializer.data][0])
    return data
