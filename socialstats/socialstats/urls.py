from django.urls import path, include
from django.contrib import admin
from social_stats.views import (
    get_channel_members,
    connect_facebook,
    facebook_callback,
    home,
    get_channel_subscriptions,
    connect_youtube,
    youtube_callback,
    connect_twitter,  # New view for Twitter authentication
    twitter_callback,  # New view for Twitter callback
)

urlpatterns = [
    path('get_channel_members/', get_channel_members, name='get_channel_members'),
    path('get_channel_subscriptions/', get_channel_subscriptions, name='get_channel_subscriptions'),
    path('connect_facebook/', connect_facebook, name='connect_facebook'),
    path('facebook_callback/', facebook_callback, name='facebook_callback'),
    path('connect_youtube/', connect_youtube, name='connect_youtube'),
    path('youtube-callback/', youtube_callback, name='youtube_callback'),
    path('connect_twitter/', connect_twitter, name='connect_twitter'),  # New URL for Twitter authentication
    path('twitter-callback/', twitter_callback, name='twitter_callback'),  # New URL for Twitter callback
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
