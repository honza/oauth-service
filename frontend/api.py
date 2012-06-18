import os
import json
import requests
from oauth_hook import OAuthHook

FRONTEND_KEY = os.environ.get('FRONTEND_KEY', None)
FRONTEND_SECRET = os.environ.get('FRONTEND_SECRET', None)
DATA_HOST = "http://127.0.0.1:8000"


assert FRONTEND_KEY and FRONTEND_SECRET


def make_request(user, url):
    OAuthHook.consumer_key = FRONTEND_KEY
    OAuthHook.consumer_secret = FRONTEND_SECRET
    hook = OAuthHook(access_token=user['access_token'],
            access_token_secret=user['access_token_secret'], header_auth=True)
    client = requests.session(hooks={'pre_request': hook})

    response = client.get(DATA_HOST + url)

    if response.status_code != 200:
        return None

    return json.loads(response.content)


def authenticate(username, password):
    credentials = {
        'username': username,
        'password': password
    }
    response = requests.post(DATA_HOST + "/authenticate",  credentials)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data['token'], data['secret']
    else:
        return None, None

# API methods ----------------------------------------------------------------


def get_color(user):
    return make_request(user, "/")
