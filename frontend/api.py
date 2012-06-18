import json
import requests
from oauth_hook import OAuthHook

FRONTEND_KEY = '12b1bd1876bfe6c2cccd84a4fe2a8bc82159ec13'
FRONTEND_SECRET = 'c4e0573cb3f2539a381b771033bfc866d4239011'
DATA_HOST = "http://127.0.0.1:8000"


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


def get_greeting(user):
    return make_request(user, "/")
