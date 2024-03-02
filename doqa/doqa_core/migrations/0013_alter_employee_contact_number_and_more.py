# Generated by Django 5.0.2 on 2024-03-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doqa_core', '0012_employee_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='contact_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='driver_license_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registration_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
