#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from .conf import settings


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")
