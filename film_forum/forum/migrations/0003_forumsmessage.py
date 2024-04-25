# Generated by Django 5.0.2 on 2024-04-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_delete_forumsmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumsMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_id', models.IntegerField()),
                ('m_id', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'ForumsMessage',
                'managed': True,
                'unique_together': {('f_id', 'm_id', 'time', 'content')},
            },
        ),
    ]
