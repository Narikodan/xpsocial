# Generated by Django 5.0.1 on 2024-01-30 05:21

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SocialMediaCredentials",
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
                ("api_id", models.CharField(max_length=50)),
                ("api_hash", models.CharField(max_length=50)),
                ("channel_username", models.CharField(max_length=100)),
                ("facebook_client_id", models.CharField(max_length=50)),
                ("facebook_client_secret", models.CharField(max_length=50)),
                ("facebook_redirect_uri", models.URLField()),
            ],
        ),
    ]
