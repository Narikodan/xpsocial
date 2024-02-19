import asyncio
import json
import os
import base64
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telethon.sync import TelegramClient
import google
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests_oauthlib import OAuth1
from .models import SocialMediaCredentials, TwitterTemporaryData

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def get_channel_members(request):
    try:
        credentials = SocialMediaCredentials.objects.get(pk=2)  # Use the correct primary key

        # Explicitly set up an event loop for Telethon using syncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient('session_name', credentials.api_id, credentials.api_hash, loop=loop)
        client.start(bot_token=credentials.bot_token)  # Add a bot_token field in the SocialMediaCredentials model

        # Get members count
        members_count = client.get_participants(credentials.channel_username)
        print(f"Number of members in the channel: {len(members_count)}")

        # Get members list
        member_list = [member.username for member in members_count if member.username is not None]
        print("Member list:")
        print(member_list)

        client.disconnect()

    except SocialMediaCredentials.DoesNotExist:
        print("SocialMediaCredentials record does not exist.")
        member_list = []

    except Exception as e:
        print(f"Error: {e}")
        member_list = []

    return render(request, 'members.html', {'member_list': member_list})

@csrf_exempt
def connect_facebook(request):
    # Redirect users to Facebook for authentication
    credentials = SocialMediaCredentials.objects.get(pk=2)  # Assuming you have only one record for now
    return redirect(f"https://www.facebook.com/v19.0/dialog/oauth?client_id={credentials.facebook_client_id}&redirect_uri={credentials.facebook_redirect_uri}&scope=user_likes")

@csrf_exempt
def facebook_callback(request):
    # Extract code from the request
    code = request.GET.get('code', '')

    # Exchange the authorization code for an access token
    credentials = SocialMediaCredentials.objects.get(pk=2)  # Assuming you have only one record for now
    facebook_token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "client_id": credentials.facebook_client_id,
        "client_secret": credentials.facebook_client_secret,
        "redirect_uri": credentials.facebook_redirect_uri,
        "code": code,
    }

    response = requests.post(facebook_token_url, data=params)

    if response.status_code == 200:
        access_token = response.json()["access_token"]

        # Use the obtained access token to get user's liked pages
        liked_pages_url = f"https://graph.facebook.com/v19.0/me?fields=likes&access_token={access_token}"
        liked_pages_response = requests.get(liked_pages_url)

        # ...

        if liked_pages_response.status_code == 200:
            liked_pages_data = liked_pages_response.json()

            # Extract the "data" array
            data_array = liked_pages_data.get('likes', {}).get('data', [])

            if data_array:
                # Extract the "name" and "id" of each page in the data array
                pages_list = [{"name": page.get('name', ''), "id": page.get('id', '')} for page in data_array]

                return JsonResponse({"liked_pages": pages_list})
            else:
                return JsonResponse({"error": "No liked pages found for XPayBack"}, status=500)
        else:
            error_message = liked_pages_response.json().get('error', 'Unknown error')
            return JsonResponse({"error": f"Failed to fetch liked pages from Facebook: {error_message}"}, status=500)

    else:
        return JsonResponse({"error": "Failed to obtain access token from Facebook"}, status=500)

@csrf_exempt
def get_channel_subscriptions(request):
    try:
        credentials = SocialMediaCredentials.objects.get(pk=2)  # Use the correct primary key

        # Check if YouTube credentials exist
        if credentials.youtube_refresh_token:
            # Refresh the access token using the refresh token
            youtube_credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
                client_id=credentials.youtube_client_id,
                client_secret=credentials.youtube_client_secret,
                token=credentials.youtube_token,
                refresh_token=credentials.youtube_refresh_token,
                token_uri='https://accounts.google.com/o/oauth2/token'
            )

            if youtube_credentials.expired:
                youtube_credentials.refresh(requests.Request())
        else:
            # If YouTube credentials don't exist, redirect the user to authenticate
            return redirect('connect_youtube')

        # Build the YouTube API client
        youtube_api = build('youtube', 'v3', credentials=youtube_credentials)

        # Retrieve the user's subscriptions
        subscriptions = youtube_api.subscriptions().list(
            part='snippet',
            mine=True
        ).execute()

        # Extract the channel information
        channels_list = [{
            'title': item['snippet']['title'],
            'channel_id': item['snippet']['resourceId']['channelId']
        } for item in subscriptions['items']]

        return render(request, 'subscriptions.html', {'channels_list': channels_list})

    except SocialMediaCredentials.DoesNotExist:
        print("SocialMediaCredentials record does not exist.")
        channels_list = []

    except HttpError as e:
        print(f"Error: {e}")
        channels_list = []

    return render(request, 'subscriptions.html', {'channels_list': channels_list})

@csrf_exempt
def connect_youtube(request):
    credentials = SocialMediaCredentials.objects.get(pk=2)  # Assuming you have only one record for now
    youtube_scopes = ['https://www.googleapis.com/auth/youtube.readonly']

    # Get the path to the client secrets file
    client_secrets_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

    # Create OAuth2 flow from client secrets file
    youtube_flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path,
        scopes=youtube_scopes,
        redirect_uri='http://localhost:8000/youtube-callback/'  # Add this line
    )

    # Generate the authorization URL
    authorization_url, state = youtube_flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    # Convert necessary fields to a JSON-compatible format
    credentials_data = {
        'youtube_client_id': credentials.youtube_client_id,
        'youtube_client_secret': credentials.youtube_client_secret,
        'youtube_token': credentials.youtube_token,
        'youtube_refresh_token': credentials.youtube_refresh_token,
    }

    # Save the state and credentials to the session for later verification
    request.session['youtube_auth_state'] = state
    request.session['youtube_credentials'] = json.dumps(credentials_data)
    request.session.save()

    return redirect(authorization_url)

@csrf_exempt
def youtube_callback(request):
    credentials = SocialMediaCredentials.objects.get(pk=2)  # Assuming you have only one record for now

    # Get the authorization code from the request
    authorization_code = request.GET.get('code', None)
        # Get the path to the client secrets file
    client_secrets_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

    if authorization_code:
        # Create OAuth2 flow from client secrets file
        youtube_flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_path,  # Update with the correct path
            scopes=['https://www.googleapis.com/auth/youtube.readonly'],
            redirect_uri='http://localhost:8000/youtube-callback/'
        )

        # Fetch tokens using the authorization code
        youtube_flow.fetch_token(code=authorization_code)

        # Create a YouTube API service client
        youtube_credentials = youtube_flow.credentials
        youtube = build('youtube', 'v3', credentials=youtube_credentials)

        # Get the list of subscribed channels
        subscriptions_response = youtube.subscriptions().list(
            part='snippet',
            mine=True
        ).execute()

        # Extract channel titles from the response
        channel_titles = [item['snippet']['title'] for item in subscriptions_response.get('items', [])]

        # Return the list of subscribed channels as JSON response
        return JsonResponse({'channel_titles': channel_titles})
    else:
        # Handle error or redirect to an error page
        return HttpResponse("Error: Authorization code not found.")

@csrf_exempt
def connect_twitter(request):
    try:
        # Assuming you have a SocialMediaCredentials record for Twitter with the primary key 2
        credentials = SocialMediaCredentials.objects.get(pk=2)

        # Twitter API endpoint for obtaining a request token
        twitter_request_token_url = "https://api.twitter.com/oauth/request_token"

        # Set up OAuth1 authentication parameters
        oauth = OAuth1(
            client_key=credentials.twitter_api_key,
            client_secret=credentials.twitter_api_secret_key,
            callback_uri='http://localhost:8000/twitter-callback/'  # Update with your actual callback URL
        )

        # Request a request token
        token_response = requests.post(twitter_request_token_url, auth=oauth)

        if token_response.status_code == 200:
            # Extract request token from the response
            request_tokens = dict(item.split("=") for item in token_response.text.split("&"))

            # Store the user's Twitter ID and request token in the database temporarily
            TwitterTemporaryData.objects.create(
                user_id=request_tokens.get('user_id', ''),
                request_token=request_tokens.get('oauth_token', '')
            )

            # Redirect the user to Twitter for authentication
            twitter_auth_url = f"https://api.twitter.com/oauth/authorize?oauth_token={request_tokens['oauth_token']}"
            return redirect(twitter_auth_url)

        else:
            # Debugging statement
            print(f"Failed to obtain request token. Status code: {token_response.status_code}")
            return JsonResponse({"error": "Failed to obtain request token from Twitter"}, status=500)

    except SocialMediaCredentials.DoesNotExist:
        # Debugging statement
        print("SocialMediaCredentials record does not exist.")
        return JsonResponse({"error": "SocialMediaCredentials record does not exist."}, status=500)

    except Exception as e:
        # Debugging statement
        print(f"Error: {e}")
        return JsonResponse({"error": f"Unexpected error: {e}"}, status=500)

@csrf_exempt
def twitter_callback(request):
    try:
        # Retrieve Twitter credentials
        credentials = SocialMediaCredentials.objects.get(pk=2)  # Use the correct primary key

        # Retrieve Twitter user ID from temporary data
        temp_data = TwitterTemporaryData.objects.get(request_token=request.GET.get('oauth_token'))
        user_id = temp_data.user_id

        # Set up the Twitter API endpoint to fetch the user's following list
        twitter_api_url = f"https://api.twitter.com/2/users/{user_id}/following"

        # Set up the headers with OAuth 2.0 App-only authentication
        headers = {
            'Authorization': f"Bearer {credentials.twitter_bearer_token}",
            'Content-Type': 'application/json',
        }

        # Make the request to Twitter API
        response = requests.get(twitter_api_url, headers=headers)

        if response.status_code == 200:
            # Parse the JSON response
            following_list = response.json().get('data', [])

            return JsonResponse({"following_list": following_list})
        else:
            # Handle error response
            error_message = response.json().get('errors', [{'message': 'Unknown error'}])[0]['message']
            return JsonResponse({"error": f"Failed to fetch following list from Twitter: {error_message}"}, status=500)

    except SocialMediaCredentials.DoesNotExist:
        return JsonResponse({"error": "SocialMediaCredentials record does not exist."}, status=500)

    except TwitterTemporaryData.DoesNotExist:
        return JsonResponse({"error": "TwitterTemporaryData record does not exist."}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"Error: {e}"}, status=500)
