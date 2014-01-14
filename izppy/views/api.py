#-*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~~~~

    api views: provide all tables json data.

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, request, g, jsonify
from izppy.models.cases import Case
from izppy.models.codes import Code
from izppy.models.task import Task, Taskcount
from izppy.models.admin import ModuleType, Machine
from izppy.models.users import User
from izppy.permissions import auth, adm
from izppy.extensions import cache
default = {"aaData": {}}

api = Module(__name__)


@cache.memoize(timeout=84600)
def cache_case_json_byauthorid(id):
    return list(Case.query.getall_by_authorid(g.user.id).jsonify())


@api.route("/case_authorid/json/")
@auth.require(401)
def case_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_byauthorid(g.user.id)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_public(user):
    return list(Case.query.public(user).jsonify())


@api.route("/case_public/json/")
@auth.require(401)
def case_json_public():
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_public(g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_public_single(user):
    return list(Case.query.public_single(user).jsonify())


@api.route("/case_public_single/json/")
@auth.require(401)
def case_json_public_single():
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_public_single(g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_private(user):
    return list(Case.query.private(user).jsonify())


@api.route("/case_private/json/")
@auth.require(401)
def case_json_private():
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_private(g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_module_public(id, user):
    return list(Case.query.getpublic_by_moudletype(id, user).jsonify())


@api.route("/case_module_public/<int:module_id>/json/")
@auth.require(401)
def case_json_module_public(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_module_public(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_module_public_single(id, user):
    return list(Case.query.getpublic_single_by_moudletype(id, user).jsonify())


@api.route("/case_module_public_single/<int:module_id>/json/")
@auth.require(401)
def case_json_module_public_single(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_module_public_single(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_module_private(id, user):
    return list(Case.query.getprivate_by_moudletype(id, user).jsonify())


@api.route("/case_module_private/<int:module_id>/json/")
@auth.require(401)
def case_json_module_private(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_module_private(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_parent_public(id, user):
    return list(Case.query.getpublic_by_parentid(id, user).jsonify())


@api.route("/case_parent_public/<int:module_id>/json/")
@auth.require(401)
def case_json_parent_public(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_parent_public(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_parent_public_single(id, user):
    return list(Case.query.getpublic_single_by_parentid(id, user).jsonify())


@api.route("/case_parent_public_single/<int:module_id>/json/")
@auth.require(401)
def case_json_parent_public_single(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_parent_public_single(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_case_json_parent_private(id, user):
    return list(Case.query.getprivate_by_parentid(id, user).jsonify())


@api.route("/case_parent_private/<int:module_id>/json/")
@auth.require(401)
def case_json_parent_private(module_id):
    if g.user and request.headers.get("Referer"):
        cases = cache_case_json_parent_private(module_id, g.user)
        return jsonify(aaData=cases)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_code_json_byauthorid(id):
    return list(Code.query.getall_by_authorid(id).jsonify())


@api.route("/code_authorid/json/")
@auth.require(401)
def code_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        codes = cache_code_json_byauthorid(g.user.id)
        return jsonify(aaData=codes)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_byauthorid(id):
    return list(Task.query.getall_by_authorid(id).jsonify())


@api.route("/task_authorid/json/")
@auth.require(401)
def task_json_byauthorid():
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_byauthorid(g.user.id)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_public(user):
    return list(Task.query.public(user).jsonify())


@api.route("/task_public/json/")
@auth.require(401)
def task_json_public():
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_public(g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_public_single(user):
    return list(Task.query.public_single(user).jsonify())


@api.route("/task_public_single/json/")
@auth.require(401)
def task_json_public_single():
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_public_single(g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_private(user):
    return list(Task.query.private(user).jsonify())


@api.route("/task_private/json/")
@auth.require(401)
def task_json_private():
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_private(g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_module_public(id, user):
    return list(Task.query.getpublic_by_moudletype(id, user).jsonify())


@api.route("/task_module_public/<int:module_id>/json/")
@auth.require(401)
def task_json_module_public(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_module_public(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_module_public_single(id, user):
    return list(Task.query.getpublic_single_by_moudletype(id, user).jsonify())


@api.route("/task_module_public_single/<int:module_id>/json/")
@auth.require(401)
def task_json_module_public_single(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_module_public_single(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_module_private(id, user):
    return list(Task.query.getprivate_by_moudletype(id, user).jsonify())


@api.route("/task_module_private/<int:module_id>/json/")
@auth.require(401)
def task_json_module_private(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_module_private(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_parent_public(id, user):
    return list(Task.query.getpublic_by_parentid(id, user).jsonify())


@api.route("/task_parent_public/<int:module_id>/json/")
@auth.require(401)
def task_json_parent_public(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_parent_public(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_parent_public_single(id, user):
    return list(Task.query.getpublic_single_by_parentid(id, user).jsonify())


@api.route("/task_parent_public_single/<int:module_id>/json/")
@auth.require(401)
def task_json_parent_public_single(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_parent_public_single(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_task_json_parent_private(id, user):
    return list(Task.query.getprivate_by_parentid(id, user).jsonify())


@api.route("/task_parent_private/<int:module_id>/json/")
@auth.require(401)
def task_json_parent_private(module_id):
    if g.user and request.headers.get("Referer"):
        tasks = cache_task_json_parent_private(module_id, g.user)
        return jsonify(aaData=tasks)
    return jsonify(default)


@api.route("/taskcount/<int:task_id>/json/")
#@auth.require(401)
def task_json_stat(task_id):
    if request.headers.get("Referer"):
        taskcounts = Taskcount.query.data(task_id).jsonify()
        return jsonify(aaData=list(taskcounts))
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_code_json_all():
    return list(Code.query.getall().jsonify())


@api.route("/code_all/json/")
@auth.require(401)
def code_json_all():
    if g.user and request.headers.get("Referer"):
        codes = cache_code_json_all()
        return jsonify(aaData=codes)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_code_json_module(id):
    return list(Code.query.getall_by_moudleid(id).jsonify())


@api.route("/code_module/<int:module_id>/json/")
@auth.require(401)
def code_json_module(module_id):
    if g.user and request.headers.get("Referer"):
        codes = cache_code_json_module(module_id)
        return jsonify(aaData=codes)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_code_json_parent(id):
    return list(Code.query.getall_by_parentid(id).jsonify())


@api.route("/code_parent/<int:module_id>/json/")
@auth.require(401)
def code_json_parent(module_id):
    if g.user and request.headers.get("Referer"):
        codes = cache_code_json_parent(module_id)
        return jsonify(aaData=codes)
    return jsonify(default)


@api.route("/user/json/")
@auth.require(401)
@adm.require(401)
def user_json():
    if g.user and request.headers.get("Referer"):
        users = User.query.getall().jsonify()
        return jsonify(aaData=list(users))
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_machine_json():
    return list(Machine.query.getall().jsonify())


@api.route("/machine/json/")
@auth.require(401)
@adm.require(401)
def machine_json():
    if g.user and request.headers.get("Referer"):
        machines = cache_machine_json()
        return jsonify(aaData=machines)
    return jsonify(default)


@cache.memoize(timeout=84600)
def cache_module_json():
    return list(ModuleType.query.getall().jsonify())


@api.route("/module/json/")
@auth.require(401)
@adm.require(401)
def module_json():
    if g.user and request.headers.get("Referer"):
        modules = cache_module_json()
        return jsonify(aaData=modules)
    return jsonify(default)


@api.route("/hudson/<int:id>/json/")
@auth.require(401)
def hudson_json(id):
    if g.user and request.headers.get("Referer"):
        task = Task.query.get_or_404(id)
        return jsonify(status=task.hudson)
    return jsonify(status=0)
