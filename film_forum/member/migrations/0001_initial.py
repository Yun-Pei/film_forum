# Generated by Django 5.0.2 on 2024-04-20 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('introduction', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('img', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('star', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Movies',
                'managed': True,
            },
        ),
    ]
