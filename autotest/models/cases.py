"""
    cases.py
    ~~~~~~~~~~~

    cases table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""


from datetime import datetime
from werkzeug import cached_property
from flask.ext.principal import Permission, UserNeed
from flask.ext.sqlalchemy import BaseQuery
from autotest.extensions import db
from autotest.permissions import moderator
from autotest.models.users import User
from autotest.models.admin import ModuleType
from autotest.helpers import get_access


class CaseQuery(BaseQuery):
    def jsonify(self):
        for case in self.all():
            yield case.json

    def get_by_title(self,title):
        return self.filter(Case.title == title).first()

    def public_count(self, user=None):
        criteria = []
        if user:
            criteria.append(Case.author_id == user.id)
            criteria.append(Case.access == Case.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def private_count(self, user=None):
        criteria = []
        if user:
            criteria.append(Case.author_id == user.id)
            criteria.append(Case.access == Case.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def public(self, user=None):
        if user and user.is_moderator:
            return self.order_by(Case.id.desc())
        return self.filter(Case.access == Case.PUBLIC).order_by(Case.id.desc())

    def private(self, user=None):
        if user and user.is_moderator:
            return self.order_by(Case.id.desc())
        criteria = []
        if user:
            criteria.append(Case.author_id == user.id)
            criteria.append(Case.access == Case.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def get_by_id(self, id):
        return self.get(id)

    def getpublic_by_moudletype(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Case.module_type == id).order_by(Case.id.desc())
        criteria = [Case.module_type == id]
        criteria.append(Case.access == Case.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def getprivate_by_moudletype(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Case.module_type == id).order_by(Case.id.desc())
        criteria = [Case.module_type == id]
        if user:
            criteria.append(Case.author_id == user.id)
            criteria.append(Case.access == Case.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def getpublic_by_parentid(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Case.parent_id == id).order_by(Case.id.desc())
        criteria = [Case.parent_id == id]
        criteria.append(Case.access == Case.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def getprivate_by_parentid(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Case.parent_id == id).order_by(Case.id.desc())
        criteria = [Case.parent_id == id]
        if user:
            criteria.append(Case.author_id == user.id)
            criteria.append(Case.access == Case.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Case.id.desc())

    def getall_by_authorid(self, id):
        return self.filter(Case.author_id == id).order_by(Case.id.desc())

    def restricted_search(self, user=None):
        if user and user.is_moderator:
            return self
        criteria = [Case.access == Case.PUBLIC]
        if user:
            criteria.append(Case.author_id == user.id)
        return self.filter(reduce(db.or_, criteria)).order_by(Case.id.desc())

    def search(self, keywords, user=None):
        criteria = []
        if user and user.is_moderator:
            for keyword in keywords.split():
                keyword = '%' + keyword + '%'
                criteria.append(db.or_(Case.title.ilike(keyword),
                                Case.description.ilike(keyword),
                                Case.id.ilike(keyword)))
        else:
            for keyword in keywords.split():
                keyword = '%' + keyword + '%'
                criteria.append(db.or_(db.and_(db.or_(Case.title.ilike(keyword),
                                                      Case.description.ilike(keyword),
                                                      Case.id.ilike(keyword)),
                                               Case.access == Case.PUBLIC),
                                       db.and_(db.or_(Case.title.ilike(keyword),
                                                      Case.description.ilike(keyword),
                                                      Case.id.ilike(keyword)),
                                               Case.author_id == user.id)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct().order_by(Case.id.desc())


class Case(db.Model):
    __tablename__ = "cases"
    query_class = CaseQuery
    PER_PAGE = 20
    PUBLIC = 100
    PRIVATE = 300
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    title = db.Column(db.Unicode(200), unique=True, nullable=False)
    description = db.Column(db.UnicodeText)
    case_create_time = db.Column(db.DateTime, default=datetime.now)
    case_update_time = db.Column(db.DateTime, default=datetime.now)
    access = db.Column(db.Integer, default=PUBLIC)
    # status = db.Column(db.Boolean, default=True)
    usecase_input = db.Column(db.UnicodeText)
    usecase_output = db.Column(db.UnicodeText)
    module_type = db.Column(db.Integer,
                            db.ForeignKey(ModuleType.id, ondelete='CASCADE'),
                            nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")
    casetype = db.relation(ModuleType, innerjoin=True, lazy="joined")

    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def default(self):
            return Permission(UserNeed(self.obj.author_id)) & moderator

        @cached_property
        def view(self):
            if self.obj.access == Case.PUBLIC:
                return Permission()
            return self.default

        @cached_property
        def edit(self):
            return self.default

        @cached_property
        def delete(self):
            return self.default

    def __init__(self, *args, **kwargs):
        super(Case, self).__init__(*args, **kwargs)
        self.access = self.access or self.PUBLIC

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    author=self.author.username,
                    title=self.title,
                    description=self.description,
                    case_create_time=str(self.case_create_time),
                    case_update_time=str(self.case_update_time),
                    access=get_access(self.access),
                    usecase_input=self.usecase_input,
                    usecase_output=self.usecase_output,
                    casetype=self.casetype.name,
                    checkBox="<input type='checkbox' name='case' value='" + str(self.id) + "' />"
                    )
"""
    @cached_property
    def attach_pre_url(self):
        result = []
        if self.precondition_path:
            result = self.precondition_path.split(";").remove('')
        return result

    @cached_property
    def attach_pro_url(self):
        result = []
        if self.process_path:
            result = self.process_path.split(";").remove('')
        return result

    @cached_property
    def attach_other_url(self):
        result = []
        if self.other_path:
            result = self.other_path.split(";").remove('')
        return result
        """
