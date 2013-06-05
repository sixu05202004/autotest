# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
access = {100: "public",
          300: "private"}

role = {100: "memeber",
        200: "MODERATOR",
        300: "admin"}

result = {0:"success",
          1:"fail"}

hudson = {1:"running",
          2:"invalid",
          3:"disable",
          4:"enable"}

def get_access(id):
    return access.get(id)


def get_role(id):
    return role.get(id)


def get_result(id):
    return result.get(id)


def get_hudson(id):
    return hudson.get(id)


