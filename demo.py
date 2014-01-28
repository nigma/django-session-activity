#!/bin/env python
#-*- coding: utf-8 -*-

"""
Demo script. Run:

python.exe demo.py
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

logging.basicConfig()

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.core.wsgi import get_wsgi_application

basename = os.path.splitext(os.path.basename(__file__))[0]


def rel(*path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *path)
    ).replace("\\", "/")


if not settings.configured:
    settings.configure(
        DEBUG=True,
        TIMEZONE="UTC",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "demo.sqlite"
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.sessions",
            "django.contrib.admin",
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "session_activity"
        ],
        MIDDLEWARE_CLASSES=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "session_activity.middleware.SessionActivityMiddleware",
        ],
        TEMPLATE_DIRS=[rel("tests", "templates")],
        STATIC_ROOT=os.path.abspath(rel("tests", "static")),
        ROOT_URLCONF=basename,
        WSGI_APPLICATION="{}.application".format(basename),
        LOGIN_URL="/login/",
        STATIC_URL="/static/"
    )

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r'^admin/', include(admin.site.urls)),
    url(r"^login/$", "django.contrib.auth.views.login"),
    url(r"^", include('session_activity.urls')),
)

application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import call_command
    from django.contrib.auth.models import User
    call_command("syncdb", interactive=False)
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@test.com", "pass")
    call_command("runserver", "8000")
