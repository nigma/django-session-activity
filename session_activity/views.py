#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, View

from .activity import get_active_sessions, sign_out_other_sessions


class SessionListView(ListView):

    template_name = "session_activity/session_list.html"

    def get_queryset(self):
        return get_active_sessions(self.request.user, request=self.request)


class SignOutOtherView(View):

    success_url = reverse_lazy("session_activity_list")

    messages = {
        "signed_out": {
            "message": _("Signed out from other sessions"),
            "level": messages.SUCCESS
        },
    }

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def post(self, request, *args, **kwargs):
        self.sign_out()
        return HttpResponseRedirect(self.get_success_url())

    def sign_out(self):
        count = sign_out_other_sessions(self.request.user, request=self.request)
        if count:
            message = self.messages["signed_out"]
            messages.add_message(self.request, **message)


session_list_view = login_required(SessionListView.as_view())
sign_out_other_view = csrf_protect(login_required(SignOutOtherView.as_view()))
