# Generated by Django 5.0.2 on 2024-03-10 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doqa_core', '0014_trip_route_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='distance',
            field=models.FloatField(default=None, null=True),
        ),
    ]
