#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .conf import settings


class SessionActivity(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    session_key     = models.CharField(_("session key"), max_length=40)
    created_at      = models.DateTimeField(auto_now_add=True)


def create_session_activity(request, user, **kwargs):
    """
    Start session activity tracking for newly logged-in user.
    """
    session_key = request.session.session_key
    if user.is_authenticated():
        SessionActivity.objects.get_or_create(user=user, session_key=session_key)


def destroy_session_activity(user, request, **kwargs):
    """
    Destroy session activity record.

    Should be called when user logs out or when a session is deactivated.
    """
    session_key = request.session.session_key
    if user.is_authenticated():
        SessionActivity.objects.filter(user=user, session_key=session_key)


user_logged_in.connect(create_session_activity)
user_logged_out.connect(destroy_session_activity)
