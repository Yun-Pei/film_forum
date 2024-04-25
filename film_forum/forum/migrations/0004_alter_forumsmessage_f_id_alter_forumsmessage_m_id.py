# Generated by Django 5.0.2 on 2024-04-23 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_forumsmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumsmessage',
            name='f_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forums'),
        ),
        migrations.AlterField(
            model_name='forumsmessage',
            name='m_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='forum.forums'),
        ),
    ]
