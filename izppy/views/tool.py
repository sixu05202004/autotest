#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-*- coding: utf-8 -*-
"""
    tool.py
    ~~~~~~~~~

    tool views: provide all kinds of tools.

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, flash, redirect, url_for, render_template, request
from izppy.permissions import auth
from izppy.models.admin import ModuleType
from izppy.forms import PmcForm, UlcIPUAForm, UlcCookieForm
from izppy.helpers import make_userid, make_ua, make_userid_ua, ip_to, clear
from izppy.config import defaultconfig
import redis
import time


tool = Module(__name__)

map_table = {"-": "",
             "&": "",
             "^": ""}


def clear_cache():
    clear(defaultconfig().CACHE_REDIS_HOST, defaultconfig().CACHE_REDIS_PORT,
          defaultconfig().CACHE_REDIS_DB)


@tool.route("/pmc/", methods=("GET", "POST"))
@auth.require(401)
def pmc():
    parents = ModuleType.query.get_parent()
    form = PmcForm(next=request.referrer)
    if form.validate_on_submit():
        try:
            port = int(form.port.data)
        except:
            port = 6379
        password = None
        if form.password.data:
            password = form.password.data
        r = redis.StrictRedis(host=form.host.data, port=port, db=form.db.data, password=password, socket_timeout=100)

        try:
            value = form.context.data.replace("-", map_table.get("-"))
            value = value.replace("&", map_table.get("&"))
            value = value.replace("^", map_table.get("^"))
            r.set(form.url.data, value)
            flash(u"Add redis successfully!", "success")
            return redirect(url_for("index.index"))
        except:
            flash(u"Add redis fail!", "error")

    return render_template('tool/pmc.html', form=form, parents=parents)


@tool.route("/ulccookie/", methods=("GET", "POST"))
@auth.require(401)
def ulc_cookie():
    parents = ModuleType.query.get_parent()
    form = UlcCookieForm(next=request.referrer)
    if form.validate_on_submit():
        try:
            port = int(form.port.data)
        except:
            port = 6379
        password = None
        if form.password.data:
            password = form.password.data
        r = redis.StrictRedis(host=form.host.data, port=port, db=0, password=password, socket_timeout=100)
        try:
            if not form.udc_cate.data and not form.policy.data:
                flash(u"Because udc_cate and policy are None, Nothing need Do!", "success")
                return redirect(url_for("index.index"))
            userid = make_userid(id=form.type.data, cookie=form.cookie.data)
            if form.udc_cate.data:
                r.set(userid, form.udc_cate.data)
            if form.policy.data:
                policy = form.policy.data.split(';')
                time_flag = int(time.time()) + 7 * 24 * 60 * 60 * 60 * 60 * 60 * 60
                r = redis.StrictRedis(host=form.host.data, port=port, db=2, password=password, socket_timeout=100)
                for item in policy:
                    r.zadd(userid, time_flag, item)

            flash(u"Add redis successfully!", "success")
            return redirect(url_for("index.index"))
        except:
            flash(u"Add redis fail!", "error")

    return render_template('tool/ulccookie.html', form=form, parents=parents)


@tool.route("/ulcua/", methods=("GET", "POST"))
@auth.require(401)
def ulc_ua_ip():
    parents = ModuleType.query.get_parent()
    form = UlcIPUAForm(next=request.referrer)
    if form.validate_on_submit():
        try:
            port = int(form.port.data)
        except:
            port = 6379
        password = None
        if form.password.data:
            password = form.password.data
        r = redis.StrictRedis(host=form.host.data, port=port, db=0, password=password, socket_timeout=100)
        try:
            if not form.udc_cate.data and not form.policy.data:
                flash(u"Because udc_cate and policy are None, Nothing need Do!", "success")
                return redirect(url_for("index.index"))
            ua = make_ua(form.ua.data.strip())
            value = ip_to(form.ip.data.strip())
            ip = hex(value).lstrip('0x').zfill(8).upper()

            userid = make_userid_ua(ip, ua)
            print userid
            if form.udc_cate.data:
                r.set(userid, form.udc_cate.data)
            r = redis.StrictRedis(host=form.host.data, port=port, db=6, password=password, socket_timeout=100)
            r.set(value, "00100000" + ip)
            if form.policy.data:
                policy = form.policy.data.split(';')

                time_flag = int(time.time()) + 7 * 24 * 60 * 60 * 60 * 60 * 60 * 60
                r = redis.StrictRedis(host=form.host.data, port=port, db=2, password=password, socket_timeout=100)
                for item in policy:
                    r.zadd(userid, time_flag, item)

            flash(u"Add redis successfully!", "success")
            return redirect(url_for("index.index"))
        except:
            flash(u"Add redis fail!", "error")
    return render_template('tool/ulcua.html', form=form, parents=parents)
