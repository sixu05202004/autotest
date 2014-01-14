# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~

    flask extension initialization.(not contain flask-principal!)

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, ARCHIVES
from izppy.hudson import Hudson
from izppy.config import defaultconfig


mail = Mail()
db = SQLAlchemy()
cache = Cache()
up = UploadSet('files', ARCHIVES)
hud = Hudson(url=defaultconfig().HUDSON)
