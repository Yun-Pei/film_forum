# Generated by Django 5.0.2 on 2024-05-27 20:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0013_delete_mpreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='likemovies',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]