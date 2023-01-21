from django.urls import path

from . import views

urlpatterns = [
    path('api/', views.get),
    path('', views.home),
]
