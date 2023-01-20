from rest_framework import serializers
from .models import City


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city', 'temperature', 'temperature_feelslike', 'precipitation', 'wind', 'cloudiness']
