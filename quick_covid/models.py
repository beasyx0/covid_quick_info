import uuid
from django.db import models
from django.utils import timezone


class TimeStamped(models.Model):
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
