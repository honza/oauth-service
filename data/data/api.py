import json

from functools import wraps
from django.http import HttpResponse, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

import oauth2 as oauth

from models import User


CONSUMERS = getattr(settings, 'CONSUMERS', {})


server = oauth.Server(signature_methods={
    'HMAC-SHA1': oauth.SignatureMethod_HMAC_SHA1()
})


def get_consumer(consumer_key):
    """
    Extract consumer information from settings
    """
    try:
        obj = CONSUMERS[consumer_key]
    except KeyError:
        return None

    if obj['active']:
        return oauth.Consumer(consumer_key, obj['secret'])

    return None


def get_user_by_token(token):
    """
    Look up user by ``token``.  Implement a real method.
    """
    try:
        return User.objects.get(token=token)
    except User.DoesNotExist:
        return None


def _check_request(request):
    """
    Verify that the flask ``request`` is properly signed and the user making it
    is authorized to proceed.
    """
    auth_header = {}
    parameters = {}

    if 'Authorization' in request.META:
        auth_header = {'Authorization': request.META['Authorization']}
    elif 'HTTP_AUTHORIZATION' in request.META:
        auth_header =  {'Authorization': request.META['HTTP_AUTHORIZATION']}

    if request.method == "POST" and \
        (request.META.get('CONTENT_TYPE') == "application/x-www-form-urlencoded" \
            or request.META.get('SERVER_NAME') == 'testserver'):
        parameters = dict(request.REQUEST.items())

    r = oauth.Request.from_request(request.method,
            request.build_absolute_uri(),
            headers=auth_header, parameters=parameters,
            query_string=request.META.get('QUERY_STRING', ''))

    access_token = r.get_parameter('oauth_token')
    consumer_key = r.get_parameter('oauth_consumer_key')

    frontend_consumer = get_consumer(consumer_key)

    user = get_user_by_token(access_token)

    if not user:
        return False, None

    token = oauth.Token(user.token, user.secret)


    try:
        server.verify_request(r, frontend_consumer, token)
        return True, user
    except:
        return False, None


def oauth_protected(f):
    """
    Flask view decorator.  Make sure that incoming OAuth request is valid.
    """
    @wraps(f)
    def decorated_view(request, *args, **kwargs):
        allowed, user = _check_request(request)
        if allowed:
            return f(request, user, *args, **kwargs)
        else:
            raise HttpResponseForbidden()
    return decorated_view


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        content = json.dumps(data, cls=DjangoJSONEncoder)
        super(JsonResponse, self).__init__(content=content,
                mimetype='application/json')


def jsonify(func):
    """
    If view returned serializable dict, returns JsonResponse with this dict
    as content.

    example:

        @ajax_request
        def my_view(request):
            return {'news_titles': 2}
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, dict):
            return JsonResponse(response)
        else:
            return response
    return wrapper
