#-*- coding: utf-8 -*-
"""
    index.py
    ~~~~~~~~~

    index views

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template
from autotest.models.admin import ModuleType
from autotest.permissions import auth
#from autotest.extensions import cache


idx = Module(__name__)


@idx.route("/index/")
@auth.require(401)
#@cache.cached(timeout=300)
def index():
    parents = ModuleType.query.get_parent()
    return render_template('index.html', parents=parents)
