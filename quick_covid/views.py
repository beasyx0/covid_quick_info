from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from quick_covid.models import Location
from quick_covid.forms import LocationForm, LocationSelectForm
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import localtime


def index(request):
    all_location_names = Location.objects.values('name')
    form = LocationSelectForm(request.POST or None, initial='')
    if request.method == 'POST':
        if form.is_valid():
            location = form.cleaned_data['location']
    if request.method == 'GET':
        location = get_object_or_404(Location, name='Global')
        messages.success(request, f'Last updated: {localtime(location.updated).strftime("%m/%d/%Y @ %H:%M:%S %p")}')
    last_updated = location.updated
    context = {
        'all_location_names': all_location_names,
        'location': location,
        'form': form,
        'last_updated': last_updated,
    }
    return render(request, 'quick_covid/index.html', context)


def fetch_location(request):
    if request.method == 'POST' and request.is_ajax():
        public_id = request.POST.get('public_id', None)
        location = get_object_or_404(Location, public_id=public_id)
        res = {
            'name': location.name,
            'cases_total': location.cases_total,
            'cases_total_per_100k': location.cases_total_per_100k,
            'cases_newly_reported_last_7_days': location.cases_newly_reported_last_7_days,
            'cases_newly_reported_last_24_hours': location.cases_newly_reported_last_24_hours,
            'deaths_total': location.deaths_total,
            'deaths_total_per_100k': location.deaths_total_per_100k,
            'deaths_newly_reported_last_7_days': location.deaths_newly_reported_last_7_days,
            'deaths_newly_reported_last_24_hours': location.deaths_newly_reported_last_24_hours,
        }
        return JsonResponse(res, status=200)
    else:
        return HttpResponseBadRequest()


import re
def my_intcomma(value):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    This function is located in django.contrib.humanize
    """
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return my_intcomma(new)


def fetch_location_2(request):
    if request.method == 'POST' and request.is_ajax():
        location_name = request.POST.get('location')
        location = get_object_or_404(Location, name=location_name)
        res = {
            'name': location.name,
            'cases_total': my_intcomma(location.cases_total),
            'cases_total_per_100k': my_intcomma(location.cases_total_per_100k),
            'cases_newly_reported_last_7_days': my_intcomma(location.cases_newly_reported_last_7_days),
            'cases_newly_reported_last_24_hours': my_intcomma(location.cases_newly_reported_last_24_hours),
            'deaths_total': my_intcomma(location.deaths_total),
            'deaths_total_per_100k': my_intcomma(location.deaths_total_per_100k),
            'deaths_newly_reported_last_7_days': my_intcomma(location.deaths_newly_reported_last_7_days),
            'deaths_newly_reported_last_24_hours': my_intcomma(location.deaths_newly_reported_last_24_hours),
        }
        return JsonResponse(res, status=200)
    else:
        return HttpResponseBadRequest()



