# Generated by Django 4.2.2 on 2023-06-14 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LoadedCost", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="hourly_rate",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="salary",
        ),
    ]
