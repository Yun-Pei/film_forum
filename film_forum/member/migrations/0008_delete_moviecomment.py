# Generated by Django 5.0.4 on 2024-05-08 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("member", "0007_moviecomment_time"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MovieComment",
        ),
    ]