#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib import admin

from .models import SessionActivity, SecurityHistory


class SessionActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at")
    list_select_related = True


class SecurityHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "username", "action", "ip", "session_key", "user_agent", "created_at")
    list_select_related = True


admin.site.register(SessionActivity, SessionActivityAdmin)
admin.site.register(SecurityHistory, SecurityHistoryAdmin)
