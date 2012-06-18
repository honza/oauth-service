from django.db import models
from uuid import uuid4
import hashlib


def _get_rand_hash():
    uid = uuid4()
    return hashlib.sha1(str(uid)).hexdigest()


def generate_token_secret():
    return _get_rand_hash(), _get_rand_hash()


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=200, blank=True)
    secret = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.token:
            self.token, self.secret = generate_token_secret()
        return super(User, self).save(*args, **kwargs)
