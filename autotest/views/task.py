#-*- coding: utf-8 -*-
"""
    task.py
    ~~~~~~~~~

    task views: task manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, flash, g, redirect, url_for, render_template, session
from autotest.forms import AddTaskForm, EditTaskForm
from autotest.models.task import Task, Taskcount
from autotest.models.cases import Case
from autotest.models.admin import ModuleType
from autotest.models.codes import Code
from autotest.extensions import db, hud
from flask.ext.babel import lazy_gettext as _
from autotest.permissions import auth, adm
from datetime import datetime
#from werkzeug import secure_filename
from autotest.hudson import HudsonException
from autotest.hudson_template import build
from autotest.config import defaultconfig
#import os

task = Module(__name__)


@task.route("/showtask/")
@auth.require(401)
def showtask():
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('task/showalltask.html', parents=parents, nodes=nodes)


@task.route("/<int:parent_id>/<int:module_id>/showtask/")
@auth.require(401)
def showtask_module(module_id, parent_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(parent_id)
    return render_template('task/showmoduletask.html', module_id=module_id,
                           parents=parents, nodes=nodes)


@task.route("/parent/<int:module_id>/showtask/")
@auth.require(401)
def showtask_parent(module_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(module_id)
    return render_template('task/showparenttask.html', module_id=module_id,
                           parents=parents, nodes=nodes)

'''
@task.route("/search/<int:page>/")
@task.route("/search/")
@auth.require(401)
def search(page=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    searchword = request.args.get('s', '')
    if not searchword:
        tasks = Task.query.restricted_search(g.user).\
            paginate(page, Task.PER_PAGE)
        page_url = lambda page: url_for('task.search', page=page)
        return render_template('task/searchtask.html', page_obj=tasks,
                               page_url=page_url, parents=parents, nodes=nodes)
    tasks = Task.query.search(searchword, g.user).paginate(page, Task.PER_PAGE)
    page_url = lambda page: url_for('task.search', page=page)
    return render_template('task/searchtask.html', page_obj=tasks,
                           page_url=page_url, parents=parents, nodes=nodes)

'''


@task.route("/<int:id>/showstat/")
#@auth.require(401)
def showstat(id=1):
    parents = ModuleType.query.get_parent()
    nodes = Taskcount.query.data(id)
    task = Task.query.get_or_404(id)
    HUDSON = defaultconfig().HUDSON
    LOG_URL = defaultconfig().LOG_URL

    task = Task.query.get_or_404(id)
    #task.permissions.view.test(403)
    return render_template('task/showstat.html', task=task, parents=parents,\
                            nodes=nodes, HUDSON=HUDSON, LOG_URL=LOG_URL)


@task.route("/<name>/showstat_name/")
#@auth.require(401)
def showstatByname(name):
    task = Task.query.get_by_name(name)
    if task:
        parents = ModuleType.query.get_parent()
        nodes = Taskcount.query.data(task.id)
        HUDSON = defaultconfig().HUDSON
        LOG_URL = defaultconfig().LOG_URL

        task = Task.query.get_or_404(task.id)
        #task.permissions.view.test(403)
        return render_template('task/showstat.html', task=task,parents=parents,\
                               nodes=nodes, HUDSON=HUDSON,  LOG_URL=LOG_URL)
    return render_template('errors/403.html')


@task.route("/showsingle/<int:id>/")
@auth.require(401)
def showsingle(id=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    task = Task.query.get_or_404(id)
    task.permissions.view.test(403)
    return render_template('task/showsingle.html', task=task,
                           parents=parents, nodes=nodes)


@task.route("/addtask/", methods=("GET", "POST"))
@auth.require(401)
def addtask():
    form = AddTaskForm()
    form.moduletype_id.choices = [(item.id, _(item.name))
                                  for item in ModuleType.query.
                                  get_allsubmodule()]
    form.case_list.choices = [(item.id, _(item.title))
                              for item in Case.query.public()]
    form.code_list.choices = [(item.id, _(item.name))
                              for item in Code.query.getall()]

    if form.validate_on_submit():
        task = Task()
        task.author_id = g.user.id
        form.populate_obj(task)
        case = []
        for case_id in form.case_list.data:
            case.append(Case.query.get_or_404(case_id))
        code = []
        for code_id in form.code_list.data:
            code.append(Code.query.get_or_404(code_id))
        task.case = case
        task.code = code
        task.parent_id = ModuleType.query.get_or_404(form.moduletype_id.data).parent_id
        '''
        message = dict(name=task.email_topic, start_time=task.runtime, \
                       svn=task.svn, mail_address=task.email,
                       shell=task.command + '\n' + defaultconfig().HUDSOM_DATA
                    %(request.headers.get("host")))
        '''
        if task.code:
            code = []
            for i in task.code:
                code.append(i.path)
            for j in code:
                print 'hg clone %s'%(j)
            print ['hg clone %s' %(i) for i in code]
        if task.svn:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=[eval(i) for i in task.svn.split(';')],
                           mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' + task.command)
        else:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=task.svn,mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' + task.command)

        if task.access == 100:
            try:
                hud.create_job(task.name, build(message))
                task.hudson = 4
                db.session.add(task)
                db.session.commit()
                flash(_(u"Add {0} successfully!".format(task.name)), "success")
            except HudsonException:
                task.hudson = 2
                task.access = 300
                db.session.add(task)
                db.session.commit()
                flash(_(u"Add {0} fail!".format(task.name)), "fail")
            finally:
                return redirect(url_for("task.showtask"))
        else:
            task.hudson = 2
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("task.showtask"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('task/task.html', form=form, parents=parents,
                           nodes=nodes)


@task.route("/addtask_case/", methods=("GET", "POST"))
@auth.require(401)
def addtask_case():
    if session[g.user.username]:
        task = Task()
        task.case_list = session[g.user.username]
    form = EditTaskForm(task)
    form.moduletype_id.choices = [(item.id, _(item.name))
                                  for item in ModuleType.query.
                                  get_allsubmodule()]
    form.case_list.choices = [(item.id, _(item.title))
                              for item in Case.query.public()]
    form.code_list.choices = [(item.id, _(item.name))
                              for item in Code.query.getall()]

    if form.validate_on_submit():
        task.author_id = g.user.id
        form.populate_obj(task)
        case = []
        for case_id in form.case_list.data:
            case.append(Case.query.get_or_404(case_id))
        code = []
        for code_id in form.code_list.data:
            code.append(Code.query.get_or_404(code_id))
        task.case = case
        task.code = code
        task.parent_id = ModuleType.query.get_or_404(form.moduletype_id.data).parent_id
        if task.svn:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=[eval(i) for i in task.svn.split(';')],
                           mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' + task.command)
        else:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=task.svn, mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' + task.command)
        if task.access == 100:
            try:
                hud.create_job(task.name, build(message))
                task.hudson = 4
                db.session.add(task)
                db.session.commit()
                flash(_(u"Add {0} successfully!".format(task.name)), "success")
            except HudsonException:
                task.hudson = 2
                task.access = 300
                db.session.add(task)
                db.session.commit()
                flash(_(u"Add {0} fail!".format(task.name)), "fail")
            finally:
                return redirect(url_for("task.showtask"))
        else:
            task.hudson = 2
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("task.showtask"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('task/task.html', form=form, parents=parents,
                           nodes=nodes)


@task.route("/<int:task_id>/deltask/", methods=("GET", "POST"))
@auth.require(401)
def deltask(task_id):
    task = Task.query.get_or_404(task_id)
    task.permissions.delete.test(403)
    db.session.delete(task)
    db.session.commit()
    flash(_(u"{0} has been deleted".format(task.name)), "success")
    try:
        hud.delete_job(task.name)
    except HudsonException:
        pass
    finally:
        return redirect(url_for("task.showtask"))


@task.route("/<int:task_id>/edittask/", methods=("GET", "POST"))
@auth.require(401)
def edittask(task_id):
    task = Task.query.get_or_404(task_id)
    task.permissions.edit.test(403)
    tmp_case = db.engine.execute("select cases_id from task_case where task_id=%s" % (task_id)).fetchall()
    tmp_code = db.engine.execute("select code_id from task_code where task_id=%s" % (task_id)).fetchall()
    if tmp_case:
        task.case_list = list(zip(*tmp_case)[0])
    if tmp_code:
        task.code_list = list(zip(*tmp_code)[0])
    form = EditTaskForm(task)
    form.moduletype_id.choices = [(item.id, _(item.name))
                                  for item in ModuleType.query.
                                  get_allsubmodule()]
    form.case_list.choices = [(item.id, _(item.title))
                              for item in Case.query.public()]
    form.code_list.choices = [(item.id, _(item.name))
                              for item in Code.query.getall()]
    if form.validate_on_submit():
        '''
        if task.author_id != g.user.id:
            task.author_id = g.user.id
        '''
        task.task_update_time = datetime.now()
        form.populate_obj(task)
        if task.parent_id != ModuleType.query.\
                get_or_404(form.moduletype_id.data).parent_id:
            task.parent_id = ModuleType.query.\
                get_or_404(form.moduletype_id.data).parent_id
        case = []
        for case_id in form.case_list.data:
            case.append(Case.query.get_or_404(case_id))
        code = []
        for code_id in form.code_list.data:
            code.append(Code.query.get_or_404(code_id))
        task.case = case
        task.code = code
        if task.svn:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=[eval(i) for i in task.svn.split(';')],
                           mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' + task.command)
        else:
            message = dict(name=task.email_topic, start_time=task.runtime,
                           svn=task.svn, mail_address=task.email,\
                           shell="\n".join(['hg clone %s' %(j) for j in [i.path for i in task.code]]) + '\n' +task.command)
        hudson_job = hud.job_exists(task.name)
        if task.access == 100:
            if hudson_job:
                try:
                    hud.reconfig_job(task.name, build(message))
                    task.hudson = 4
                except HudsonException:
                    hud.disable_job(task.name)
                    task.hudson = 2
                finally:
                    db.session.add(task)
                    db.session.commit()
                    flash(_(u"Update {0} successfully!".format(task.name)), "success")
                    return redirect(url_for("task.showtask"))

            else:
                try:
                    hud.create_job(task.name, build(message))
                    task.hudson = 4
                    db.session.add(task)
                    db.session.commit()
                    flash(_(u"Update {0} successfully!".format(task.name)), "success")
                except HudsonException:
                    task.hudson = 2
                finally:
                    db.session.add(task)
                    db.session.commit()
                    flash(_(u"Update {0} successfully!".format(task.name)), "success")
                    return redirect(url_for("task.showtask"))
        else:
            try:
                hud.delete_job(task.name)
            except HudsonException:
                pass
            finally:
                task.hudson = 2
                db.session.add(task)
                db.session.commit()
                db.engine.execute("delete from task_count where task_id=%s" % (task_id))
                flash(_(u"Update {0} successfully!".format(task.name)), "success")
                return redirect(url_for("task.showtask"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('task/edittask.html', form=form, parents=parents,
                           nodes=nodes)


@task.route("/<int:task_id>/runtask/", methods=("GET", "POST"))
@auth.require(401)
def runtask(task_id):
    task = Task.query.get_or_404(task_id)
    task.permissions.run.test(403)
    try:
        hud.build_job(task.name)
        flash(_(u"Run {0} successfully!".format(task.name)), "success")
    except HudsonException:
        flash(_(u"Run {0} fail!".format(task.name)), "fail")
    finally:
        db.engine.execute("update task set hudson=1 where id=%s" % (task_id))
        return redirect(url_for("task.showtask"))


@task.route("/<int:task_id>/starttask/", methods=("GET", "POST"))
@auth.require(401)
def starttask(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        hud.enable_job(task.name)
        db.engine.execute("update task set hudson=4 where id=%s" % (task_id))
        flash(_(u"Start {0} sucessfully!".format(task.name)), "success")
    except HudsonException:
        flash(_(u"Start {0} fail".format(task.name)), "fail")
    finally:
        return redirect(url_for("task.showtask"))


@task.route("/<int:task_id>/stoptask/", methods=("GET", "POST"))
@auth.require(401)
def stoptask(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        hud.disable_job(task.name)
        db.engine.execute("update task set hudson=3 where id=%s" % (task_id))
        flash(_(u"Stop {0} sucessfully!".format(task.name)), "success")
    except HudsonException:
        flash(_(u"Stop {0} fail".format(task.name)), "fail")
    finally:
        return redirect(url_for("task.showtask"))


@task.route("/<int:task_id>/showresult/")
@task.route("/<int:task_id>/showresult/<int:page>/")
@auth.require(401)
def showresult(task_id, page=1):
    taskcounts = Taskcount.query.get_by_taskid(task_id).\
        paginate(page, Taskcount.PER_PAGE, error_out=False)
    page_url = lambda page: url_for('task.showresult', task_id=task_id, page=page)
    return render_template('task/showresult.html', page_obj=taskcounts,
                           page_url=page_url)


@task.route("/monitor/")
@auth.require(401)
@adm.require(401)
def monitor():
    '''
    hudson_data = [[1, 'a', 19], [2, 'b', 16]] //[[task_id,task_name,build_id]]
    '''
    task_info = db.engine.execute("select id,name  from  task").fetchall()
    hudson_data = []
    for task in task_info:
        try:
            temp1 = hud.get_job_info(task[1])
            if temp1["nextBuildNumber"]:
                temp2 = [task[0], task[1], temp1["nextBuildNumber"] - 1]
                hudson_data.append(temp2)
            else:
                pass
        except HudsonException:
            pass
    for data in hudson_data:
        if data[2] > 1:
            next = Taskcount.query.get_task_next(data[0])
            case_all = len(Task.query.get_by_id(data[0]).case)
            if next:
                start = next.build_id
                for build_id in range(start + 1, data[2]):
                    if Taskcount.query.get_task_build(data[0], build_id):
                        pass
                    else:
                        Taskcount1 = Taskcount(task_id=data[0], case_all=case_all, case_pass=0,
                                               case_fail=case_all, result=1, build_id=build_id)
                        db.session.add(Taskcount1)
                        db.session.commit()
                Taskcount2 = Taskcount.query.get_task_build(data[0], start)
                Taskcount2.next = 0
                Taskcount3 = Taskcount.query.get_task_build(data[0], data[2] - 1)
                Taskcount3.next = 1
                db.session.add(Taskcount2)
                db.session.add(Taskcount3)
                db.session.commit()
            else:
                for build_id in range(1, data[2]):
                    if Taskcount.query.get_task_build(data[0], build_id):
                        pass
                    else:
                        Taskcount4 = Taskcount(task_id=data[0], case_all=case_all, case_pass=0,
                                               case_fail=case_all, result=1, build_id=build_id)
                        db.session.add(Taskcount4)
                        db.session.commit()
                Taskcount5 = Taskcount.query.get_task_build(data[0], data[2] - 1)
                Taskcount5.next = 1
                db.session.add(Taskcount5)
                db.session.commit()
    return "ok"
