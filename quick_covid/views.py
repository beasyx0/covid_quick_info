import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from quick_covid.models import Location
from quick_covid.forms import LocationForm, LocationSelectForm
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import localtime


def index(request):
    '''Main view for quick covid'''
    all_location_names = Location.objects.values('name')
    location = get_object_or_404(Location, name='Global')
    form = LocationSelectForm(request.POST or None, initial='')
    # if request.method == 'POST':
    #     if form.is_valid():
    #         location = form.cleaned_data['location']
    messages.success(request, f'Last updated: {localtime(location.updated).strftime("%m/%d/%y %I:%M %p")}')
    last_updated = location.updated
    context = {
        'all_location_names': all_location_names,
        'location': location,
        'form': form,
        'last_updated': last_updated,
    }
    return render(request, 'quick_covid/index.html', context)


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


def fetch_location(request):
    '''Function to return a Location object from an AJAX call'''
    if request.method == 'POST' and request.is_ajax():
        location_name = request.POST.get('location')
        location = get_object_or_404(Location, name=location_name)
        res = {
            'country_image_html': location.get_flag_image_html(),
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



def fetch_most_deaths(request):
    '''Function that return values for use with Chart.js charts'''
    labels = []
    data = []
    locations = Location.objects.values().exclude(name='Global').order_by('-deaths_total')[:10]
    for loc in locations:
        labels.append(loc['name'])
        data.append(loc['deaths_total'])
    return JsonResponse(data={
                            'labels': labels,
                            'data': data,
                        })


def fetch_most_deaths_last_day(request):
    '''Function that returns the top 10 most deaths in the last 24hr'''
    labels = []
    data = []
    locations = Location.objects.values().exclude(name='Global').order_by('-deaths_newly_reported_last_24_hours')[:10]
    for loc in locations:
        labels.append(loc['name'])
        data.append(loc['deaths_newly_reported_last_24_hours'])
    return JsonResponse(data={
                            'labels': labels,
                            'data': data,
                        })