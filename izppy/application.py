# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask.ext.principal import Principal, identity_loaded
from flask.ext.babel import Babel
from flask import Flask, request, g, render_template
from izppy.models import User
from izppy.extensions import cache, db, mail, up
from flaskext.uploads import configure_uploads
from izppy.config import defaultconfig
from izppy.helpers import get_access, get_role, get_hudson, get_result
from izppy import views

__all__ = ["setup_app"]
DEFAULT_NAME = "izppy"
DEFAULT_MODULES = (
                  (views.idx, ""),
                  (views.admin, "/admin"),
                  (views.account, "/account"),
                  (views.case, "/case"),
                  (views.task, "/task"),
                  (views.about, "/about"),
                  (views.code, "/code"),
                  (views.notice, "/notice"),
                  (views.stat, "/stat"),
                  (views.api, "/api"),
                  (views.tool, "/tool"),
                  (views.docs, "/docs")

)


def setup_app(config=None, app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_NAME
    if modules is None:
        modules = DEFAULT_MODULES
    app = Flask(app_name)
    init_configure_app(app, config)
    init_logging_app(app)
    init_errorhandle(app)
    init_extensions(app)
    init_before_handlers(app)
    init_register_views(app, modules)
    configure_template_filters(app)
    #with app.test_request_context():
    #    db.create_all()
    return app


def init_configure_app(app, config):
    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object(defaultconfig())
    app.config.from_envvar('IZPPY_SET', silent=True)


def init_register_views(app, modules):
    for module, prefix in modules:
        app.register_module(module, url_prefix=prefix)


def configure_template_filters(app):

    @app.template_filter()
    def access(id):
        return get_access(id)

    @app.template_filter()
    def role(id):
        return get_role(id)

    @app.template_filter()
    def hudson(id):
        return get_hudson(id)

    @app.template_filter()
    def result(id):
        return get_result(id)


def init_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    init_identity(app)
    init_i18n(app)
    init_upload(app)


def init_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def init_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.gen_identity(identity)


def init_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        lan = app.config.get('ACCEPT_LANGUAGES', ['zh'])
        return request.accept_languages.best_match(lan)


def init_upload(app):
    configure_uploads(app, up)


def init_errorhandle(app):

    @app.errorhandler(404)
    def page_not_find(error):
        return render_template('errors/404.html')

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html')

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html')


def init_logging_app(app):
    if app.debug:
        return

    #mail log
    mail_handler = SMTPHandler(app.config['MAILHOST'],
                               app.config['DEFAULT_MAIL_SENDER'],
                               app.config['DEFAULT_MAIL_RECEIVER'],
                               'application error',
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    #debug log
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    debug_log = os.path.join(app.root_path,
                             app.config['DEBUG_LOG'])

    debug_handler = RotatingFileHandler(debug_log, maxBytes=100000,
                                        backupCount=5)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    app.logger.addHandler(debug_handler)

    #error log
    error_log = os.path.join(app.root_path,
                             app.config['ERROR_LOG'])

    error_handler = RotatingFileHandler(error_log, maxBytes=100000,
                                        backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)
