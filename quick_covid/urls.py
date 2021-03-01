from django.contrib import admin
from django.urls import path, include

from quick_covid.views import index, fetch_location, fetch_deaths


app_name = "quick_covid"

urlpatterns = [
	path('', index, name='index'),
	path('fetch-location/', fetch_location, name='fetch-location'),
	path('fetch-deaths/', fetch_deaths, name='fetch-deaths'),
]
