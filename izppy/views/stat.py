#-*- coding: utf-8 -*-
"""
    stat.py
    ~~~~~~~~~

    stat views: provide report function

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, jsonify, g, render_template
from izppy.models.task import Taskcount, Task
from izppy.models.codes import Code
from izppy.models.cases import Case
from izppy.models.admin import ModuleType
from izppy.permissions import auth
from izppy.extensions import cache
default = [['public', 0], ['private', 0], ['all', 0]]

stat = Module(__name__)


@stat.route("/data/<int:task_id>/")
def data(task_id):
    result = Taskcount.query.data(task_id).all()[:14]

    categories = [str(item.timing) for item in result]
    data_pass = [item.case_pass for item in result]
    data_fail = [item.case_fail for item in result]

    return jsonify(categories=categories, data=(data_pass, data_fail))


@stat.route('/case_author/')
@cache.cached(timeout=84600)
def case_author():
    if g.user:
        total = Case.query.count()
        if total:
            public = Case.query.public_count(g.user).count() / float(total)
            private = Case.query.private_count(g.user).count() / float(total)
            other = 1 - public - private
            return jsonify(data=[['Your Public', public], ['Your Private', private],
                                 ['Other Users', other]])
    return jsonify(data=default)


@stat.route('/task_author/')
@cache.cached(timeout=84600)
def task_author():
    if g.user:
        total = Task.query.count()
        if total:
            public = Task.query.public_count(g.user).count() / float(total)
            private = Task.query.private_count(g.user).count() / float(total)
            other = 1 - public - private
            return jsonify(data=[['Your Public', public], ['Your Private', private],
                                 ["Other Users", other]])
    return jsonify(data=default)


@stat.route('/code_author/')
@cache.cached(timeout=84600)
def code_author():
    if g.user:
        total = Code.query.getall().count()
        if total:
            your = Code.query.getall_by_authorid(g.user.id).count() / float(total)
            other = 1 - your
            return jsonify(data=[['Yours', your], ['Other Users', other]])
    return jsonify(data=default)


@stat.route('/case_public/')
@cache.cached(timeout=84600)
def case_public():
    tmp = []
    if g.user:
        total = Case.query.public().count()
        if total:
            public = ModuleType.query.get_allsubmodule()
            for item in public:
                public_module = item.name
                public_proportion = Case.query.getpublic_by_moudletype(item.id).count() / float(total)
                s = [public_module, public_proportion]
                if not s in tmp:
                    tmp.append(s)
        return jsonify(data=tmp)
    return jsonify(data=default)


@stat.route('/task_public')
@cache.cached(timeout=84600)
def task_public():
    tmp = []
    if g.user:
        total = Task.query.public().count()
        if total:
            public = Task.query.getpublic_by_moudletype(ModuleType.id)
            for item in public:
                public_module = ModuleType.query.get_by_id(item.moduletype_id).name
                public_proportion = Task.query.getpublic_by_moudletype(item.moduletype_id).count() / float(total)
                s = [public_module, public_proportion]
                if not s in tmp:
                    tmp.append(s)
        return jsonify(data=tmp)
    return jsonify(data=default)


@stat.route('/task/')
@auth.require(401)
@cache.cached(timeout=84600)
def task():
    parents = ModuleType.query.get_parent()
    return render_template('stat/task_stat.html', parents=parents)


@stat.route('/case/')
@auth.require(401)
@cache.cached(timeout=84600)
def case():
    parents = ModuleType.query.get_parent()
    return render_template('stat/case_stat.html', parents=parents)


@stat.route('/index/')
@auth.require(401)
@cache.cached(timeout=84600)
def index():
    parents = ModuleType.query.get_parent()
    return render_template('stat/index_stat.html', parents=parents)


@stat.route('/test')
def test():
    parents = ModuleType.query.get_parent()
    return render_template('test/test.html', parents=parents)
