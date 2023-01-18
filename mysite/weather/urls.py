from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('<city_name>', views.get_city_name),
]
