#-*- coding: utf-8 -*-
"""
    stat.py
    ~~~~~~~~~

    stat views: provide report function

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, jsonify, g, render_template
from autotest.models.task import Taskcount, Task
from autotest.models.codes import Code
from autotest.models.cases import Case
from autotest.models.admin import ModuleType
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
def code_author():
    if g.user:
        total = Code.query.getall().count()
        if total:
            your = Code.query.getall_by_authorid(g.user.id).count() / float(total)
            other = 1 - your
            return jsonify(data=[['Yours', your], ['Other Users', other]])
    return jsonify(data=default)


@stat.route('/case_public/')
def case_public():
    tmp = []
    if g.user:
        total = Case.query.public().count()
        if total:
            public = Case.query.getpublic_by_moudletype(ModuleType.id)
            for item in public:
                public_module = ModuleType.query.get_by_id(item.module_type).name
                public_proportion = Case.query.getpublic_by_moudletype(item.module_type).count() / float(total)
                s = [public_module, public_proportion]
                if not s in tmp:
                    tmp.append(s)
        return jsonify(data=tmp)
    return jsonify(data=default)


@stat.route('/task_public')
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


@stat.route('/test')
def test():
    parents = ModuleType.query.get_parent()
    return render_template('test/test.html', parents=parents)
