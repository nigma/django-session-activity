#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.db.models import get_model

from .conf import settings

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


try:
    from django.contrib.auth import get_user_model as get_auth_user_model
except ImportError:
    def get_auth_user_model():
        return get_model("auth", "User")


def get_username(user):
    if hasattr(user, "get_username"):
        return user.get_username()
    return user.username
