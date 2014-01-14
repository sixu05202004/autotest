#-*- coding: utf-8 -*-
"""
    docs.py
    ~~~~~~~~~

    docs views: docs static html manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, send_from_directory
import os

docs = Module(__name__)

basename = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]


@docs.route("/idclick/<path:filename>")
def idclick(filename="index.html"):
    return send_from_directory(basename + "/docs/idclick", filename)
