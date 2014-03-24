#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    admin.py
    ~~~~~~~~~~~

    admin table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime
from werkzeug import cached_property
from flask.ext.sqlalchemy import BaseQuery
from izppy.extensions import db, cache
#from izppy.helpers import safe
# from izppy.models.codes import Code


class ModuleTypeQuery(BaseQuery):
    '''Provide all kinds of query functions.'''

    def jsonify(self):
        '''Converted datas into JSON.'''
        for moduletype in self.all():
            yield moduletype.json

    def getall(self):
        '''Get all datas in moduletype table.'''
        return self.order_by(ModuleType.id.desc())

    def get_by_id(self, id):
        return self.get(id)

    def get_by_name(self, name):
        return self.get(name)

    @cache.memoize(timeout=84600)
    def getsubmodule_by_parentid(self, parent_id):
        return self.filter(ModuleType.parent_id == parent_id).all()

    @cache.cached(timeout=84660, key_prefix='parent')
    def get_parent(self):
        return self.filter(ModuleType.parent_id == 0).all()

    @cache.cached(timeout=84660, key_prefix='submodule')
    def get_allsubmodule(self):
        return self.filter(ModuleType.parent_id != 0).all()

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(ModuleType.name.ilike(keyword),
                                   ModuleType.description.ilike(keyword),
                                   ModuleType.id.ilike(keyword),
                                   ModuleType.parent_id.ilike(keyword)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()


class ModuleType(db.Model):
    __tablename__ = "moduletype"
    query_class = ModuleTypeQuery
    PER_PAGE = 20
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, default=0, nullable=False)
    name = db.Column(db.Unicode(30), unique=True, nullable=False)
    description = db.Column(db.UnicodeText)
    type_create_time = db.Column(db.DateTime, default=datetime.now)
    type_update_time = db.Column(db.DateTime, default=datetime.now)
    input_template = db.Column(db.UnicodeText, nullable=False)
    output_template = db.Column(db.UnicodeText, nullable=False)
    # level = db.Column(db.Integer, default=1, nullable=False)

    def __init__(self, *args, **kwargs):
        super(ModuleType, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def json(self):
        return dict(id=self.id,
                    name=self.name,
                    description=self.description,
                    parent_id=self.parent_id,
                    input_template=self.input_template,
                    output_template=self.output_template,
                    type_create_time=str(self.type_create_time),
                    type_update_time=str(self.type_update_time))
"""
    @cached_property
    def codelist(self):
        return Code.query.filter(Code.related_module == self.id).all()
"""


class MachineQuery(BaseQuery):

    def jsonify(self):
        for machine in self.all():
            yield machine.json

    def getall(self):
        return self.order_by(Machine.id.desc())

    def get_by_id(self, id):
        return self.get(id)

    def get_all_ok(self):
        return self.filter(Machine.status == Machine.OK)

    def get_all_really(self):
        return self.filter(Machine.status == Machine.REALLY)

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Machine.name.ilike(keyword),
                                   Machine.description.ilike(keyword),
                                   Machine.id.ilike(keyword)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()


class Machine(db.Model):
    OK = 1
    REALLY = 0
    PER_PAGE = 20
    __tablename__ = "machine"
    query_class = MachineQuery
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(30), unique=True, nullable=False)
    description = db.Column(db.UnicodeText)
    m_create_time = db.Column(db.DateTime, default=datetime.now)
    m_update_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=0)
    key = db.Column(db.Unicode(100))
    username = db.Column(db.Unicode(30), nullable=False)
    password = db.Column(db.Unicode(30), nullable=False)
    url_hudson = db.Column(db.Unicode(60))
    task_count = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Machine, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def json(self):
        return dict(id=self.id,
                    name=self.name,
                    description=self.description,
                    status=self.status,
                    m_create_time=str(self.m_create_time),
                    m_update_time=str(self.m_update_time),
                    username=self.username,
                    password=self.password,
                    url_hudson=self.url_hudson,
                    task_count=self.task_count,
                    key=self.key)
