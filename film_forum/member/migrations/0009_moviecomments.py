# Generated by Django 5.0.4 on 2024-05-08 21:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("member", "0008_delete_moviecomment"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieComments",
            fields=[
                ("Comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.CharField(max_length=255)),
                ("score", models.IntegerField()),
                ("time", models.DateTimeField(default=None, null=True)),
                (
                    "mid",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="member.movies"
                    ),
                ),
                (
                    "uid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "MovieComments",
                "managed": True,
                "unique_together": {("mid", "Comment_id")},
            },
        ),
    ]
