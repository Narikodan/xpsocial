# Generated by Django 5.0.1 on 2024-02-05 07:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_stats", "0004_socialmediacredentials_twitter_api_key_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="socialmediacredentials",
            name="twitter_user_id",
        ),
        migrations.AddField(
            model_name="socialmediacredentials",
            name="twitter_access_token",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="socialmediacredentials",
            name="twitter_access_token_secret",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="socialmediacredentials",
            name="twitter_request_token",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="socialmediacredentials",
            name="twitter_request_token_secret",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
