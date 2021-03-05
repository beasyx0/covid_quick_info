from django.contrib import admin
from django.urls import path, include

from quick_covid.views import index, fetch_location, fetch_most_deaths, fetch_most_deaths_last_day


app_name = "quick_covid"

urlpatterns = [
	path('', index, name='index'),
	path('fetch-location/', fetch_location, name='fetch-location'),
	path('fetch-most-deaths/', fetch_most_deaths, name='fetch-most-deaths'),
	path('fetch-most-deaths-last-day/', fetch_most_deaths_last_day, name="fetch-most-deaths-last-day"),
]
