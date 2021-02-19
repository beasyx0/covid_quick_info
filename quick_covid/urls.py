from django.contrib import admin
from django.urls import path, include

from quick_covid.views import index


app_name = "quick_covid"

urlpatterns = [
	path('', index, name='index'),
]
