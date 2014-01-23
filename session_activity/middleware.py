#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


from .activity import update_current_session_info


class SessionActivityMiddleware(object):

    def process_request(self, request):
        update_current_session_info(request)
