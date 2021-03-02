import bs4
import requests
import uuid
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class TimeStamped(models.Model):
    '''Timestamp and public ID model for any object'''
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(editable=False, null=True)
    updated = models.DateTimeField(editable=False, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        self.updated = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)


class Location(TimeStamped):
    '''Location model. Each object is created/updated from custom management command'''
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    cases_total = models.IntegerField()
    cases_total_per_100k = models.IntegerField()
    cases_newly_reported_last_7_days = models.IntegerField()
    cases_newly_reported_last_24_hours = models.IntegerField()
    deaths_total = models.IntegerField()
    deaths_total_per_100k = models.IntegerField()
    deaths_newly_reported_last_7_days = models.IntegerField()
    deaths_newly_reported_last_24_hours = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['name']

    def get_flag_image_html(self):
        '''Fetches the url for an image of the country flag. Returns 
            formatted html for use on the front end. Returns a default globe
            image if the url cant be found'''
            # TODO: create custom command to download the image and save to db..\
            # this is broken
        try:
            url = 'https://flagpedia.net/' + self.name.lower()
            response = requests.get(url)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            image_url = soup.select(".flag-detail picture img")[0].get("src")
            full_url = 'https://flagpedia.net' + image_url
            image_html = format_html('<img class="img-fluid w-100" src="{}" alt="{}">', full_url, self.name + ' Country Flag')
            return image_html
        except:
            return format_html('<img class="img-fluid" src="{}" alt="{}">', \
                'https://www.fifighter.com/wp-content/uploads/2013/11/globe.jpg', ' Globe')
