from django.db import models


class City(models.Model):
    city = models.CharField(max_length=200)
    temperature = models.CharField(max_length=200)
    temperature_feelslike = models.CharField(max_length=200)
    precipitation = models.CharField(max_length=200)
    wind = models.CharField(max_length=200)
    cloudiness = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Town"

    def __str__(self):
        return self.city
