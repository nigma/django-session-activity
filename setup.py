#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.1.0"

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="django-session-activity",
    version=version,
    description="""List all active sessions and sign-out from all sessions opened on other computers""",
    license="MIT",
    author="Filip Wasilewski",
    author_email="en@ig.ma",
    url="https://github.com/nigma/django-session-activity",
    long_description=readme + "\n\n" + history,
    packages=[
        "session_activity",
    ],
    include_package_data=True,
    install_requires=[
        "django>=1.5.0",
        "django-appconf>=0.6",
        "python-dateutil"
    ],
    zip_safe=False,
    keywords="django-session-activity",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
