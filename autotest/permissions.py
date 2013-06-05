# -*- coding: utf-8 -*-
"""
    permissions.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.principal import Permission, RoleNeed

adm = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
auth = Permission(RoleNeed('authenticated'))
