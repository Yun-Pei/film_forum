# Generated by Django 5.0.2 on 2024-04-27 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_movies_rid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='link',
        ),
    ]