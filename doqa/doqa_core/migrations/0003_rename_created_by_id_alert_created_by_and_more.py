# Generated by Django 5.0.2 on 2024-02-14 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doqa_core', '0002_alert_created_by_id_employee_created_by_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='created_by_id',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='created_by_id',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='created_by_id',
            new_name='created_by',
        ),
    ]
