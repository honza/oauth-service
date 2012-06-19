from uuid import uuid4 as _uid
import hashlib
import random


try:
    random = random.SystemRandom()
except:
    pass


allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def _get_random_string(length=12, allowed_chars=allowed_chars):
    return ''.join([random.choice(allowed_chars) for i in range(length)])


def _get_rand_hash():
    uid = _uid()
    return hashlib.sha1(str(uid)).hexdigest()


def secret():
    """
    Generate a Flask/Django session secret
    """
    print _get_random_string(50)


def oauth():
    """
    Generate two OAuth safe sha1 hashes
    """
    print _get_rand_hash()
    print _get_rand_hash()
