#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime

from django.conf import settings

from appconf import AppConf


SESSION_IP_KEY = "_activity_ip"
SESSION_LAST_USED_KEY = "_activity_last_used"
SESSION_USER_AGENT_KEY = "_activity_user_agent"


class SessionActivityAppConf(AppConf):

    UPDATE_THROTTLE = datetime.timedelta(minutes=5)

    def configure_update_throttle(self, value):
        if isinstance(value, int):
            value = datetime.timedelta(seconds=value)
        return value
