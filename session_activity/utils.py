#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime

from dateutil import parser as date_parser


def serialize_date(d):
    """
    :type d: datetime.datetime or None
    :rtype s: str or None
    """
    if d:
        r = d.isoformat()
        if d.microsecond:
            r = r[:23] + r[26:]
        if r.endswith('+00:00'):
            r = r[:-6] + 'Z'
        return r


def deserialize_date(s):
    """
    :type s: str or None
    :rtype: datetime.datetime or None
    """
    if s:
        return date_parser.parse(s)
