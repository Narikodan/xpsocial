# models.py
from django.db import models

class SocialMediaCredentials(models.Model):
    # Fields for Facebook
    facebook_client_id = models.CharField(max_length=255)
    facebook_client_secret = models.CharField(max_length=255)
    facebook_redirect_uri = models.URLField()

    # Fields for Telegram
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=255)
    bot_token = models.CharField(max_length=255)
    channel_username = models.CharField(max_length=255)

    # Fields for YouTube
    youtube_client_id = models.CharField(max_length=255, default='')  # Specify a default value
    youtube_client_secret = models.CharField(max_length=255, default='')
    youtube_redirect_uri = models.URLField(default='https://your-default-redirect-uri.com')
    youtube_token = models.TextField(blank=True, null=True)
    youtube_refresh_token = models.CharField(max_length=255, blank=True, null=True)

    # Fields for Twitter
    twitter_api_key = models.CharField(max_length=255, default='')
    twitter_api_secret_key = models.CharField(max_length=255, default='')
    twitter_bearer_token = models.CharField(max_length=255, default='')
    twitter_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True, null=True)
    twitter_request_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_request_token_secret = models.CharField(max_length=255, blank=True, null=True)

class TwitterTemporaryData(models.Model):
    user_id = models.CharField(max_length=255)
    request_token = models.CharField(max_length=255)
