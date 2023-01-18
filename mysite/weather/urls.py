from django.urls import path

from . import views

urlpatterns = [
    path('city/', views.get_city_name),
    path('', views.home),
]
