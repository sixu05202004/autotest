#-*- coding: utf-8 -*-
"""
    index.py
    ~~~~~~~~~

    index views

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template, redirect, url_for
from izppy.models.admin import ModuleType
from izppy.permissions import auth

idx = Module(__name__)


@idx.route("/index/")
@auth.require(401)
def index():
    parents = ModuleType.query.get_parent()
    return render_template('index.html', parents=parents)


@idx.route("/")
def index_r():
    '''just for redirect!'''
    return redirect(url_for('account.login'))
