#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from collections import namedtuple

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.utils import timezone
from django.utils.importlib import import_module

from .models import SessionActivity, create_session_activity
from .utils import deserialize_date, serialize_date
from .conf import SESSION_IP_KEY, SESSION_LAST_USED_KEY, SESSION_USER_AGENT_KEY

logger = logging.getLogger("app.session_activity")

SessionInfo = namedtuple("SessionInfo", [
    "session", "session_key", "is_current",
    "ip", "last_used", "user_agent",
    "session_activity"
])


def get_session_store():
    """
    Loads session store object based on the `SESSION_ENGINE` setting.

    :rtype: :class:`django.contrib.sessions.backends.base.SessionBase`
    """
    return import_module(settings.SESSION_ENGINE).SessionStore


def is_current_session(session, request):
    """
    Checks if a given session object is the same as the on used by the request.

    :type session: :class:`django.contrib.sessions.backends.base.SessionBase`
    :type request: :class:`django.http.HttpRequest` or None
    """
    if request is not None:
        # TODO: Match by current session key or (ip, user agent) pair
        return session.session_key == request.session.session_key
    return False


def get_active_sessions(user, request=None):
    """
    Returns list of all active sessions for given user.

    :type user: django.contrib.auth.models.AbstractBaseUser
    :type request: django.http.HttpRequest
    :return: list of active session info
    :rtype: list of SessionInfo
    """
    SessionStore = get_session_store()
    active_sessions = []

    for obj in SessionActivity.objects.filter(user=user):
        # noinspection PyCallingNonCallable
        session = SessionStore(session_key=obj.session_key)

        if SESSION_KEY in session and session.get_expiry_age():
            session_info = SessionInfo(
                session=session,
                session_key=session.session_key,
                is_current=is_current_session(session, request),
                ip=session.get(SESSION_IP_KEY, None),
                last_used=deserialize_date(session.get(SESSION_LAST_USED_KEY, None)),
                user_agent=session.get(SESSION_USER_AGENT_KEY, ""),
                session_activity=obj
            )
            active_sessions.append(session_info)

    return active_sessions


def update_current_session_info(request):
    """
    Maintains and updates last used, ip and user agent fields for
    current session.

    :type request: django.http.HttpRequest
    """
    session = request.session
    now = timezone.now()
    last_used = deserialize_date(session.get(SESSION_LAST_USED_KEY, None))

    # TODO: limit to authenticated users only?
    if not last_used or (now - last_used) > settings.SESSION_ACTIVITY_UPDATE_THROTTLE:
        logger.info("Refreshing session activity")

        session[SESSION_LAST_USED_KEY] = serialize_date(now)
        session[SESSION_IP_KEY] = request.META["REMOTE_ADDR"]
        session[SESSION_USER_AGENT_KEY] = request.META.get("HTTP_USER_AGENT", "")

        user = request.user
        if user.is_authenticated():
            if not SessionActivity.objects.filter(
                    user=user, session_key=session.session_key).exists():
                # Create activity record in case it was not added on
                # user log-in (i.e. there are some old sessions in the system)
                create_session_activity(request=request, user=user)


def sign_out_other_sessions(user, request):
    """
    Deactivate all user's sessions that do not belong to
    current request

    :type user: django.contrib.auth.models.AbstractBaseUser
    :type request: django.http.HttpRequest
    """
    count = 0
    active_sessions = get_active_sessions(user=user, request=request)
    for session_info in active_sessions:
        if not session_info.is_current:
            session_info.session.flush()
            count += 1
    return count
