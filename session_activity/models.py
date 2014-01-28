#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .conf import settings
from .compat import get_username, get_auth_user_model


class SessionActivity(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    session_key     = models.CharField(_("session key"), max_length=40)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Session activity")
        verbose_name_plural = _("Session activity")


class SecurityHistoryManager(models.Manager):

    def record_action(self, request, user, action):
        """
        :type request: django.http.HttpRequest or None
        :type user: django.contrib.auth.models.AbstractBaseUser
        :param unicode action: action name
        """
        if request:
            meta = {
                "ip": request.META["REMOTE_ADDR"],
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "session_key": request.session.session_key
            }
        else:
            meta = {}

        return self.create(
            user=user,
            username=get_username(user),
            action=action,
            **meta
        )


class SecurityHistory(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    username        = models.CharField(_("username"), max_length=200)
    action          = models.CharField(_("action"), max_length=40)
    ip              = models.GenericIPAddressField(_("actor ip"), null=True)
    user_agent      = models.CharField(_("user agent"), max_length=300, default="")
    session_key     = models.CharField(_("session key"), max_length=40, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    objects         = SecurityHistoryManager()

    class Meta:
        verbose_name = _("Security history")
        verbose_name_plural = _("Security history")


def create_session_activity(request, user, **kwargs):
    """
    Start session activity tracking for newly logged-in user.

    :type request: django.http.HttpRequest or None
    :type user: django.contrib.auth.models.AbstractBaseUser
    """
    session_key = request.session.session_key
    if user.is_authenticated():
        SessionActivity.objects.get_or_create(user=user, session_key=session_key)


def destroy_session_activity(request, user, **kwargs):
    """
    Destroy session activity record.

    Should be called when user logs out or when a session is deactivated.

    :type request: django.http.HttpRequest or None
    :type user: django.contrib.auth.models.AbstractBaseUser
    """
    session_key = request.session.session_key
    if user.is_authenticated():
        SessionActivity.objects.filter(user=user, session_key=session_key)


def record_user_login_action(request, user, action="user.login", **kwargs):
    """
    :type request: django.http.HttpRequest or None
    :type user: django.contrib.auth.models.AbstractBaseUser
    """
    SecurityHistory.objects.record_action(request=request, user=user, action=action)


def record_user_create_action(instance, created, action="user.create", **kwargs):
    """
    :type instance: django.contrib.auth.models.AbstractBaseUser
    """
    if created:
        SecurityHistory.objects.record_action(request=None, user=instance, action=action)


# Session activity handlers
user_logged_in.connect(create_session_activity)
user_logged_out.connect(destroy_session_activity)

# Security history handlers
user_logged_in.connect(record_user_login_action)
post_save.connect(record_user_create_action, sender=get_auth_user_model())
