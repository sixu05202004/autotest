# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~

    users: table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime
from werkzeug import cached_property, check_password_hash,\
    generate_password_hash
from flask.ext.principal import RoleNeed, UserNeed
from flask.ext.sqlalchemy import BaseQuery
from autotest.extensions import db
from autotest.helpers import get_role


class UserQuery(BaseQuery):

    def jsonify(self):
        for user in self.all():
            yield user.json

    def gen_identity(self, identity):
        """
        Loads user from flask.ext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkeypatched to the identity instance.

        If no user found then None is returned.
        """

        try:
            user = self.get(int(identity.id))
        except (ValueError, TypeError):
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user

    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).first()

        if user and user.status:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(User.username.ilike(keyword),
                                   User.email.ilike(keyword),
                                   User.id.ilike(keyword)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()

    def get_by_id(self, id):
        return self.get(id)

    def getall(self):
        return self.order_by(User.id.desc())


class User(db.Model):

    __tablename__ = "users"
    PER_PAGE = 20
    query_class = UserQuery

    # user roles
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=True)
    user_create_time = db.Column(db.DateTime, default=datetime.now)
    user_update_time = db.Column(db.DateTime, default=datetime.now)
    role = db.Column(db.Integer, default=MEMBER)

    email_alerts = db.Column(db.Boolean, default=False)
    _password = db.Column("password", db.String(80))

    class Permissions(object):
        pass

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        if self.is_moderator:
            needs.append(RoleNeed('moderator'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        return needs

    @cached_property
    def json(self):
        return dict(id=self.id,
                    name=self.username,
                    email=self.email,
                    status=self.status,
                    user_create_time=str(self.user_create_time),
                    user_update_time=str(self.user_update_time),
                    role=get_role(self.role),
                    email_alerts=self.email_alerts)

    @property
    def is_moderator(self):
        return self.role >= self.MODERATOR

    @property
    def is_admin(self):
        return self.role >= self.ADMIN

    @property
    def is_member(self):
        return self.role == self.MEMBER
