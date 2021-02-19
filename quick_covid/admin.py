from django.contrib import admin
from quick_covid.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'updated', 'name', 'cases_total', \
        'cases_total_per_100k', 'cases_newly_reported_last_7_days', \
        'cases_newly_reported_last_24_hours', 'deaths_total', \
        'deaths_total_per_100k', 'deaths_newly_reported_last_7_days', \
        'deaths_newly_reported_last_24_hours',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 50
    list_select_related = True
    search_fields = ['date', 'updated', 'name',]
    readonly_fields = ('date', 'updated',)
    fieldsets = (
            (None, {
                'fields': ('date', 'updated', 'name', 'cases_total', \
                'cases_total_per_100k', 'cases_newly_reported_last_7_days', \
                'cases_newly_reported_last_24_hours', 'deaths_total', \
                'deaths_total_per_100k', 'deaths_newly_reported_last_7_days', \
                'deaths_newly_reported_last_24_hours',)
            }),
        )