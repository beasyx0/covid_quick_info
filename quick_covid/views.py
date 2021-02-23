from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from quick_covid.models import Location
from quick_covid.forms import LocationForm, LocationSelectForm
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import localtime


def index(request):
    form = LocationSelectForm(request.POST or None, initial='')
    if request.method == 'POST':
        if form.is_valid():
            location = form.cleaned_data['location']
    if request.method == 'GET':
        location = get_object_or_404(Location, name='Global')
        messages.success(request, f'Last updated: {localtime(location.updated).strftime("%m/%d/%Y @ %H:%M:%S %p")}')
    last_updated = location.updated
    context = {
        'location': location,
        'form': form,
        'last_updated': last_updated,
    }
    return render(request, 'quick_covid/index.html', context)


