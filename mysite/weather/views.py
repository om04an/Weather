from django.conf import settings
from django.shortcuts import render
from django.core.serializers import serialize
from .models import City
import json
from django.http import JsonResponse
import requests


def home(request):
    _update_or_create_data_db(request)
    city_and_weather_data = _data_of_all_api(request)
    return render(request, 'weather/home.html', {'data': city_and_weather_data})


def _get_name_city(request):
    if request.GET.get("city"):
        city_name = request.GET.get("city")  # Getting the name of the city from the request
    else:
        city_name = _get_name_city_by_ip()  # Getting city name by ip
    return city_name


def _get_name_city_by_ip():
    url = 'http://ip-api.com/json/'
    response = requests.get(url).text
    print(json.loads(response))
    city_name = json.loads(response)['city']

    return city_name


def _get_weather_data(city):
    api_key = settings.API_KEY
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    response = requests.get(url).text
    data = json.loads(response)

    weather_information = [data["location"]["name"],  # Selective storage of received information
                           int(data["current"]["temp_c"]),
                           int(data["current"]["feelslike_c"]),
                           data["current"]["condition"]["text"],
                           int(data["current"]["wind_kph"] * (5 / 18)),
                           data["current"]["cloud"]
                           ]

    return weather_information


def _get_city_population(city):
    api_key = settings.API_KEY_2
    url = f'https://api.api-ninjas.com/v1/city?name={city}'
    response = requests.get(url, headers={'X-Api-Key': api_key}).text
    city_population = str(json.loads(response)[0]['population'])

    return city_population


def _edit_data_db(data):
    post = City.objects.get(city=data[0])
    post.temperature = data[1]
    post.temperature_feelslike = data[2]
    post.precipitation = data[3]
    post.wind = data[4]
    post.cloudiness = data[5]
    post.population = data[6]
    post.save()


def _create_data_db(data):
    City.objects.create(city=data[0],
                        temperature=data[1],
                        temperature_feelslike=data[2],
                        precipitation=data[3],
                        wind=data[4],
                        cloudiness=data[5],
                        population=data[6]
                        )


def _data_of_all_api(request):
    city_name = _get_name_city(request)
    weather_data = _get_weather_data(city_name)  # Getting weather data
    weather_data.append(_get_city_population(weather_data[0]))  # Data aggregation

    return weather_data


def _update_or_create_data_db(request):
    city_and_weather_data = _data_of_all_api(request)

    if City.objects.filter(city=city_and_weather_data[0]):
        _edit_data_db(city_and_weather_data)  # Updating data in the database
    else:
        _create_data_db(city_and_weather_data)  # Creating data in the database


def get(request):  # API
    city = _get_name_city(request)
    city_name = _get_weather_data(city)[0]

    weather_data = City.objects.filter(city=city_name)
    weather_serialized_data = serialize('python', weather_data)

    data = {
        'weather': weather_serialized_data
    }

    return JsonResponse(data)
