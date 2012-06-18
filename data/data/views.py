from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from api import oauth_protected, jsonify
from models import User


@oauth_protected
@jsonify
def index(request, user):
    return {
        'favorite_color': user.userprofile.favorite_color
    }


@csrf_exempt
@jsonify
def authenticate(request):
    if request.method != 'POST':
        raise HttpResponseNotAllowed()

    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        raise HttpResponseForbidden()

    return {
        'token': user.token,
        'secret': user.secret
    }
