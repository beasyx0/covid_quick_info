import logging
logger = logging.getLogger(__name__)
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from quick_covid.models import Location


class Command(BaseCommand):

	'''1)Creates DataFrame from W.H.O. @ https://covid19.who.int/WHO-COVID-19-global-table-data.csv \
	   2)Drops uneccesary columns \
	   3)Iterates over the DataFrame updating or creating objects.

	   This will be a Celery Beat Periodic Task in production.'''

	help = "Command to refresh Covid data in the database"

	def handle(self, *args, **options):

		df = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-table-data.csv')

		df = df.fillna(0)

		df.drop(['WHO Region', \
				'Cases - newly reported in last 7 days per 100000 population', \
				'Deaths - newly reported in last 7 days per 100000 population', \
				'Transmission Classification'], axis=1, inplace=True)

		for i, row in df.iterrows():
			obj, created = Location.objects.update_or_create(
				name=row[0],
				defaults={
						  'cases_total': int(row[1]),
						  'cases_total_per_100k': int(row[2]),
						  'cases_newly_reported_last_7_days': int(row[3]),
						  'cases_newly_reported_last_24_hours': int(row[4]),
						  'deaths_total': int(row[5]),
						  'deaths_total_per_100k': int(row[6]),
						  'deaths_newly_reported_last_7_days': int(row[7]),
						  'deaths_newly_reported_last_24_hours': int(row[8]),
						  },
						)

			self.stdout.write(f'Successfully created {obj.name}' if created else f'Successfully updated {obj.name}')
