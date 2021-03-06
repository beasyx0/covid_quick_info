# Generated by Django 3.1.6 on 2021-02-18 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('cases_total', models.IntegerField()),
                ('cases_total_per_100k', models.IntegerField()),
                ('cases_newly_reported_last_7_days', models.IntegerField()),
                ('cases_newly_reported_last_24_hours', models.IntegerField()),
                ('deaths_total', models.IntegerField()),
                ('deaths_total_per_100k', models.IntegerField()),
                ('deaths_newly_reported_last_7_days', models.IntegerField()),
                ('deaths_newly_reported_last_24_hours', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Locations',
                'ordering': ['date'],
            },
        ),
    ]
