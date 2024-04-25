# Generated by Django 5.0.2 on 2024-04-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_movies_introduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forums',
            fields=[
                ('f_id', models.AutoField(primary_key=True, serialize=False)),
                ('m_id', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'Forums',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='movies',
            name='type',
            field=models.DateTimeField(),
        ),
    ]
