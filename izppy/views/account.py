#-*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~~~~

    account views: login, sigup, password manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, request, g, current_app, abort, redirect, \
    url_for, session, render_template
from izppy.forms import LoginForm, ChangePasswordForm, SignupForm,\
    EditMyAccountForm
from izppy.models.users import User
from izppy.extensions import db
#from flask.ext.babel import lazy_gettext as _
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from izppy.permissions import auth
from izppy.models.admin import ModuleType
from datetime import datetime

account = Module(__name__)


@account.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm(login=request.args.get("login", None),
                     next=request.args.get("next", None))

    if form.validate_on_submit():
        user, auth = \
            User.query.authenticate(form.login.data, form.password.data)
        if user and auth:
            session.permanent = form.remember

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            #need add next url
            flash(u"welcome {0}".format(user.username), "success")
            return redirect(url_for('index.index'))
        else:
            flash(u"无效登陆，请检查用户名或者密码", "error")

    return render_template('account/login.html', form=form)


@account.route("/signup/", methods=("GET", "POST"))
def signup():
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    form = SignupForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))

        flash(u"welcome {0}".format(user.username), "success")
        #need add next url
        return redirect(url_for('index.index'))

    return render_template('account/signup.html', form=form)


@account.route("/logout/")
def logout():
    flash(u"You are logout", "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('account.login'))


@account.route("/changepass/", methods=("GET", "POST"))
@auth.require(401)
def changepass():
    parents = ModuleType.query.get_parent()
    user = None
    if g.user:
        user = g.user
    if user is None:
        abort(403)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        user.user_update_time = datetime.now()
        db.session.commit()
        flash(u"Your password has been changed, "
                "please log in again", "success")

        return redirect(url_for("account.login"))
    return render_template('account/password.html', form=form, parents=parents)


@account.route("/edit/", methods=("GET", "POST"))
@auth.require(401)
def edit():
    parents = ModuleType.query.get_parent()
    form = EditMyAccountForm(g.user)
    if form.validate_on_submit():
        g.user.user_update_time = datetime.now()
        form.populate_obj(g.user)
        db.session.commit()
        flash(u"Update user information successfully", "success")
        return redirect(url_for("account.login"))
    return render_template('account/edit.html', form=form, parents=parents)
