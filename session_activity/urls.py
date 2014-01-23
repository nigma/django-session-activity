#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import session_list_view, sign_out_other_view

urlpatterns = patterns("",
    url(r"^$",                  session_list_view, name="session_activity_list"),
    url(r"^sign-out-other/",    sign_out_other_view, name="session_sign_out"),
)
