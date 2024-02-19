from django.contrib import admin
from .models import SocialMediaCredentials

@admin.register(SocialMediaCredentials)
class SocialMediaCredentialsAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'api_hash', 'channel_username', 'facebook_client_id', 'facebook_client_secret', 'facebook_redirect_uri', 'bot_token')

