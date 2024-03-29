# Generated by Django 5.0.1 on 2024-02-05 08:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_stats", "0005_remove_socialmediacredentials_twitter_user_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TwitterTemporaryData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=255)),
                ("request_token", models.CharField(max_length=255)),
            ],
        ),
    ]
