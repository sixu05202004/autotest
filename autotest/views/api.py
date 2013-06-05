#-*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~~~~

    api views: provide all tables json data.

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, request, g, jsonify
from autotest.models.cases import Case
from autotest.models.codes import Code
from autotest.models.task import Task, Taskcount
from autotest.models.admin import ModuleType, Machine
from autotest.models.users import User
from autotest.permissions import auth, adm

default = {"aaData": {}}

api = Module(__name__)


@api.route("/case_authorid/json/")
@auth.require(401)
def case_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        cases = Case.query.getall_by_authorid(g.user.id).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_public/json/")
@auth.require(401)
def case_json_public():
    if g.user and request.headers.get("Referer"):
        cases = Case.query.public(g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_private/json/")
@auth.require(401)
def case_json_private():
    if g.user and request.headers.get("Referer"):
        cases = Case.query.private(g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_module_public/<int:module_id>/json/")
@auth.require(401)
def case_json_module_public(module_id):
    if g.user and request.headers.get("Referer"):
        cases = Case.query.getpublic_by_moudletype(module_id, g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_module_private/<int:module_id>/json/")
@auth.require(401)
def case_json_module_private(module_id):
    if g.user and request.headers.get("Referer"):
        cases = Case.query.getprivate_by_moudletype(module_id, g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_parent_public/<int:module_id>/json/")
@auth.require(401)
def case_json_parent_public(module_id):
    if g.user and request.headers.get("Referer"):
        cases = Case.query.getpublic_by_parentid(module_id, g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/case_parent_private/<int:module_id>/json/")
@auth.require(401)
def case_json_parent_private(module_id):
    if g.user and request.headers.get("Referer"):
        cases = Case.query.getprivate_by_parentid(module_id, g.user).jsonify()
        return jsonify(aaData=list(cases))
    return jsonify(default)


@api.route("/code_authorid/json/")
@auth.require(401)
def code_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        codes = Code.query.getall_by_authorid(g.user.id).jsonify()
        return jsonify(aaData=list(codes))
    return jsonify(default)


@api.route("/task_authorid/json/")
@auth.require(401)
def task_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.getall_by_authorid(g.user.id).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_public/json/")
@auth.require(401)
def task_json_public():
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.public(g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_private/json/")
@auth.require(401)
def task_json_private():
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.private(g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_module_public/<int:module_id>/json/")
@auth.require(401)
def task_json_module_public(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.getpublic_by_moudletype(module_id, g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_module_private/<int:module_id>/json/")
@auth.require(401)
def task_json_module_private(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.getprivate_by_moudletype(module_id, g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_parent_public/<int:module_id>/json/")
@auth.require(401)
def task_json_parent_public(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.getpublic_by_parentid(module_id, g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/task_parent_private/<int:module_id>/json/")
@auth.require(401)
def task_json_parent_private(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = Task.query.getprivate_by_parentid(module_id, g.user).jsonify()
        return jsonify(aaData=list(tasks))
    return jsonify(default)


@api.route("/taskcount/<int:task_id>/json/")
#@auth.require(401)
def task_json_stat(task_id):
    if request.headers.get("Referer"):
        taskcounts = Taskcount.query.data(task_id).jsonify()
        return jsonify(aaData=list(taskcounts))
    return jsonify(default)
 

@api.route("/code_all/json/")
@auth.require(401)
def code_json_all():
    if g.user and request.headers.get("Referer"):
        codes = Code.query.getall().jsonify()
        return jsonify(aaData=list(codes))
    return jsonify(default)


@api.route("/code_module/<int:module_id>/json/")
@auth.require(401)
def code_json_module(module_id):
    if g.user and request.headers.get("Referer"):
        codes = Code.query.getall_by_moudleid(module_id).jsonify()
        return jsonify(aaData=list(codes))
    return jsonify(default)


@api.route("/code_parent/<int:module_id>/json/")
@auth.require(401)
def code_json_parent(module_id):
    if g.user and request.headers.get("Referer"):
        codes = Code.query.getall_by_parentid(module_id).jsonify()
        return jsonify(aaData=list(codes))
    return jsonify(default)


@api.route("/user/json/")
@auth.require(401)
@adm.require(401)
def user_json():
    if g.user and request.headers.get("Referer"):
        users = User.query.getall().jsonify()
        return jsonify(aaData=list(users))
    return jsonify(default)


@api.route("/machine/json/")
@auth.require(401)
@adm.require(401)
def machine_json():
    if g.user and request.headers.get("Referer"):
        machines = Machine.query.getall().jsonify()
        return jsonify(aaData=list(machines))
    return jsonify(default)


@api.route("/module/json/")
@auth.require(401)
@adm.require(401)
def module_json():
    if g.user and request.headers.get("Referer"):
        modules = ModuleType.query.getall().jsonify()
        return jsonify(aaData=list(modules))
    return jsonify(default)


@api.route("/hudson/<int:id>/json/")
@auth.require(401)
def hudson_json(id):
    if g.user and request.headers.get("Referer"):
        task = Task.query.get_or_404(id)
        return jsonify(status=task.hudson)
    return jsonify(status=0)

'''
@api.route("/submodule/<int:id>/json/")
@auth.require(401)
def submodule(id):
    if g.user and request.headers.get("Referer"):
        modules = ModuleType.query.getsubmodule_by_parentid(id).jsonify()
        return jsonify(aaData=list(modules))
    return jsonify(default)
'''
