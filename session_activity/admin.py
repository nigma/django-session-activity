#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib import admin

from .models import SessionActivity


class SessionActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key", "created_at")
    list_select_related = True

admin.site.register(SessionActivity, SessionActivityAdmin)
