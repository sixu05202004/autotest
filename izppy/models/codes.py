"""
    codes.py
    ~~~~~~~~~~~

    codes table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime
from werkzeug import cached_property
from flask.ext.principal import Permission, UserNeed
from flask.ext.sqlalchemy import BaseQuery
from izppy.extensions import db
from izppy.permissions import moderator
from izppy.models.users import User
from izppy.models.admin import ModuleType


class CodeQuery(BaseQuery):

    def jsonify(self):
        for code in self.all():
            yield code.json

    def getall(self):
        return self.order_by(Code.id.desc())

    def get_by_id(self, id):
        return self.get(id)

    def getall_by_moudleid(self, id):
        return self.filter(Code.related_module == id).order_by(Code.id.desc())

    def getall_by_parentid(self, id):
        return self.filter(Code.parent_id == id).order_by(Code.id.desc())

    def getall_by_authorid(self, id):
        return self.filter(Code.author_id == id).order_by(Code.id.desc())

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Code.name.ilike(keyword),
                                   Code.description.ilike(keyword),
                                   Code.id.ilike(keyword),
                                   Code.related_module.ilike(keyword)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct().order_by(Code.id.desc())
    """
    def get_by_name(self, name):
        return self.get(name)

    def get_by_module(self, related_module):

        return self.get(related_module)

    def code_list(self, modulename):
        res = self.filter(ModuleType.name == modulename)
        code_list = self.filter(Code.related_module == res.id)
        return code_list
    """


class Code(db.Model):
    __tablename__ = "code"
    query_class = CodeQuery
    PER_PAGE = 20
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    name = db.Column(db.Unicode(200), unique=True, nullable=False)
    description = db.Column(db.UnicodeText)
    code_create_time = db.Column(db.DateTime, default=datetime.now)
    code_update_time = db.Column(db.DateTime, default=datetime.now)
    related_module = db.Column(db.Integer, db.ForeignKey(ModuleType.id,
                               ondelete='CASCADE'), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    relatedmodule = db.relation(ModuleType, innerjoin=True, lazy="joined")
    path = db.Column(db.UnicodeText, nullable=False)
    # forder_name = db.Column(db.Unicode(200), nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def default(self):
            return Permission(UserNeed(self.obj.author_id)) & moderator

        @cached_property
        def edit(self):
            return self.default

        @cached_property
        def delete(self):
            return self.default

    def __init__(self, *args, **kwargs):
        super(Code, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    name=self.author.username,
                    title=self.name,
                    description=self.description,
                    code_create_time=str(self.code_create_time),
                    code_update_time=str(self.code_update_time),
                    path=self.path,
                    codetype=self.relatedmodule.name,
                    checkBox="<input type='checkbox' name='code' value='" + str(self.id) + "' onclick='setSelectCodeAll();' />")

    @cached_property
    def attach_path(self):
        result = []
        if self.path:
            result = self.path.split(";").remove('')
        return result
