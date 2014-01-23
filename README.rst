=======================
django-session-activity
=======================

.. image:: https://badge.fury.io/py/django-session-activity.png
    :target: http://badge.fury.io/py/django-session-activity

.. image:: https://pypip.in/d/django-session-activity/badge.png
    :target: https://crate.io/packages/django-session-activity?version=latest

List all active sessions and sign-out from all sessions opened on other computers.

Developed at `en.ig.ma software shop <http://en.ig.ma>`_.

Overview
--------

This app records and shows last session activity and allows users to
sign-out from all active sessions, even remote ones.

In other words, it handles the following use case:

.. pull-quote::

    You come back home and realize that you forgot to
    log out on your work/university/other remote computer. What now?

    You take a look at the recent active sessions for your account
    and click a single button to deactivate all sessions
    opened on other computers.

.. image:: http://i.imgur.com/7LOMmJL.png

Documentation
-------------

The full documentation is at http://django-session-activity.rtfd.org.

Quickstart
----------

1. Include ``django-session-activity`` in your ``requirements.txt`` file.

2. Add ``session_activity`` to ``INSTALLED_APPS`` and migrate/syncdb.

3. Add ``session_activity.middleware.SessionActivity`` to ``MIDDLEWARE_CLASSES``
   after the ``django.contrib.sessions.middleware.SessionActivityMiddleware`` and
   ``django.contrib.auth.middleware.AuthenticationMiddleware`` middleware classes.

4. Add url config for session list and sign-out views:

    .. code-block::

        url(r'^sessions/', include('session_activity.urls')),

   Then link to the main view using ``{% url "session_activity_list" %}`` template tag.

5. Optionally copy & modify the ``session_list.html`` template
   to match your look and feel expectations.

Dependencies
------------

``django-session-activity`` depends on ``django>=1.5.0``, ``django-appconf>=0.6``
and ``python-dateutil``.

License
-------

`django-session-activity` is released under the MIT license.

Other Resources
---------------

- GitHub repository - https://github.com/nigma/django-session-activity
- PyPi Package site - http://pypi.python.org/pypi/django-session-activity
