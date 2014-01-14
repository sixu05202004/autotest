#-*- coding: utf-8 -*-
"""
    case.py
    ~~~~~~~~~

    case views: case manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, flash, g, redirect, url_for, render_template, request
from izppy.forms import AddCaseForm, EditCaseForm
from izppy.models.cases import Case
from izppy.models.admin import ModuleType
from izppy.extensions import db
from flask.ext.babel import lazy_gettext as _
from izppy.permissions import auth
from izppy.views.tool import clear_cache
#from izppy.extensions import cache
from datetime import datetime
case = Module(__name__)


@case.route("/showcase/")
@auth.require(401)
def showcase():
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('case/showallcase.html', parents=parents, nodes=nodes)


@case.route("/<int:parent_id>/<int:module_id>/showcase/")
@auth.require(401)
def showcase_module(module_id, parent_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(parent_id)
    return render_template('case/showmodulecase.html', module_id=module_id,
                           parents=parents, nodes=nodes)


@case.route("/parent/<int:module_id>/showcase/")
@auth.require(401)
#@cache.cached(timeout=84600)
def showcase_parent(module_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(module_id)
    return render_template('case/showparentcase.html', module_id=module_id,
                           parents=parents, nodes=nodes)

'''
@case.route("/search/<int:page>/")
@case.route("/search/")
@auth.require(401)
def search(page=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    searchword = request.args.get('s', '')
    if not searchword:
        cases = Case.query.restricted_search(g.user).\
            paginate(page, Case.PER_PAGE)
        page_url = lambda page: url_for('case.search', page=page)
        return render_template('case/searchcase.html', page_obj=cases,
                               page_url=page_url, parents=parents, nodes=nodes)
    cases = Case.query.search(searchword, g.user).paginate(page, Case.PER_PAGE)
    page_url = lambda page: url_for('case.search', page=page)
    return render_template('case/searchcase.html', page_obj=cases,
                           page_url=page_url, parents=parents, nodes=nodes)

'''


@case.route("/showsingle/<int:id>/")
@auth.require(401)
def showsingle(id=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    case = Case.query.get_or_404(id)
    case.permissions.view.test(403)
    return render_template('case/showsingle.html', case=case,
                           parents=parents, nodes=nodes)


@case.route("/addcase/", methods=("GET", "POST"))
@auth.require(401)
def addcase():
    form = AddCaseForm(next=request.referrer)
    temp = [(0, _(u'请选择所属模块'))]

    form.module_type.choices = temp + [(item.id, _(item.name))
                                       for item in ModuleType.query.
                                       get_allsubmodule()]

    if form.validate_on_submit():
        case = Case()
        """
        if form.attach_pre.has_file():
            filename = up.save(form.attach_pre.data)
            case.precondition_path = unicode(filename)
        if form.attach_process.has_file():
            filename = up.save(form.attach_process.data)
            case.process_path = unicode(filename)
        if form.attach_other.has_file():
            filename = up.save(form.attach_other.data)
            case.other_path = unicode(filename)
        """
        case.author_id = g.user.id
        form.populate_obj(case)
        if case.module_type:
            case.parent_id = ModuleType.query.get_or_404(form.module_type.data).\
                parent_id
            db.session.add(case)
            db.session.commit()
            clear_cache()
            flash(u"Add {0} successfully!".format(case.title), "success")
            return redirect(form.next.data or url_for("case.showcase"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('case/case.html', form=form, parents=parents,
                           nodes=nodes)


@case.route("/<int:case_id>/delcase/", methods=("GET", "POST"))
@auth.require(401)
def delcase(case_id):
    case = Case.query.get_or_404(case_id)
    case.permissions.delete.test(403)
    db.session.delete(case)
    db.session.commit()
    clear_cache()
    flash(u"{0} has been deleted".format(case.title), "success")
    return redirect(request.referrer or url_for("case.showcase"))


@case.route("/<int:case_id>/editcase/", methods=("GET", "POST"))
@auth.require(401)
def editcase(case_id):
    case = Case.query.get_or_404(case_id)
    case.permissions.edit.test(403)
    form = EditCaseForm(case, next=request.referrer)
    #print form.module_type.data
    form.module_type.choices = [(item.id, _(item.name))
                                for item in ModuleType.query.
                                get_allsubmodule()]
    if form.validate_on_submit():
        """
        if form.attach_pre.has_file():
            filename = up.save(form.attach_pre.data)
            case.precondition_path = unicode(filename)
        if form.attach_process.has_file():
            filename = up.save(form.attach_process.data)
            case.process_path = unicode(filename)
        if form.attach_other.has_file():
            filename = up.save(form.attach_other.data)
            case.other_path = unicode(filename)
        if case.author_id != g.user.id:
            case.author_id = g.user.id
        """
        form.populate_obj(case)
        if case.parent_id != ModuleType.query.\
                get_or_404(form.module_type.data).parent_id:
            case.parent_id = ModuleType.query.\
                get_or_404(form.module_type.data).parent_id
        case.case_update_time = datetime.now()
        db.session.add(case)
        db.session.commit()
        clear_cache()
        flash(u"Update {0} successfully!".format(case.title), "success")
        return redirect(form.next.data or url_for("case.showcase"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('case/editcase.html', form=form, parents=parents,
                           nodes=nodes)


@case.route("/<int:case_id>/copycase/", methods=("GET", "POST"))
def copycase(case_id):
    case = Case.query.get_or_404(case_id)
    case.title = None
    form = EditCaseForm(case, next=request.referrer)
    #attention performance refresh
    db.session.refresh(case)
    #print form.module_type.data
    form.module_type.choices = [(item.id, _(item.name))
                                for item in ModuleType.query.
                                get_allsubmodule()]
    if form.validate_on_submit():
        new_case = Case()
        form.populate_obj(new_case)
        print new_case.title
        new_case.author_id = g.user.id
        if new_case.parent_id != ModuleType.query.\
                get_or_404(form.module_type.data).parent_id:
            new_case.parent_id = ModuleType.query.\
                get_or_404(form.module_type.data).parent_id
        new_case.case_create_time = datetime.now()
        new_case.case_update_time = datetime.now()
        db.session.add(new_case)
        db.session.commit()
        clear_cache()
        flash(u"Copy {0} successfully!".format(new_case.title), "success")
        return redirect(form.next.data or url_for("case.showcase"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('case/editcase.html', form=form, parents=parents,
                           nodes=nodes)