#-*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~

    admin views: login, sigup, password manage,
    module manage, code manage, machine manage and so on

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, g, current_app, redirect, \
    url_for, render_template
from autotest.forms import EditAccountForm, AddModuleForm, \
    AddMachineForm, EditMachineForm, EditModuleForm
from autotest.models.users import User
from autotest.models.admin import ModuleType, Machine
from autotest.extensions import db
from flask.ext.babel import lazy_gettext as _
from flask.ext.principal import identity_changed, AnonymousIdentity
from autotest.permissions import auth, adm
from datetime import datetime
admin = Module(__name__)


@admin.route("/showuser/")
@auth.require(401)
@adm.require(401)
def showuser():
    parents = ModuleType.query.get_parent()
    return render_template('admin/showuser.html', parents=parents)


@admin.route("/<int:user_id>/deluser/", methods=("POST", "GET"))
@auth.require(401)
@adm.require(401)
def deluser(user_id):
    user = User.query.get_or_404(user_id)

    if user_id == g.user.id:
        db.session.delete(g.user)
        db.session.commit()

        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())

        flash(_(u"Your account has been deleted"), "success")

        return redirect(url_for("account.login"))
    else:
        db.session.delete(user)
        db.session.commit()
        """
        identity_changed.send(current_app._get_current_object(),
                            identity=AnonymousIdentity())
        """
        flash(_(u"{0} has been deleted".format(user.username)), "success")
        return redirect(url_for("admin.showuser"))
    return redirect(url_for("admin.showuser"))


@admin.route("/<int:user_id>/edituser/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def edituser(user_id):
    user = User.query.get_or_404(user_id)
    form = EditAccountForm(user)
    if form.validate_on_submit():
        user.user_update_time = datetime.now()
        form.populate_obj(user)
        db.session.commit()
        if user_id == g.user.id:
            flash(_(u"Update your account successfully"), "success")
            return redirect(url_for("account.login"))
        else:
            flash(_(u"Update {0} successfully".format(user.username)),
                  "success")
    else:
        parents = ModuleType.query.get_parent()
        # return redirect(url_for("admin.showuser"))
        return render_template('admin/edituser.html', form=form,
                               parents=parents)

    return redirect(url_for("admin.showuser"))


@admin.route("/showmachine/")
@auth.require(401)
@adm.require(401)
def showmachine():
    parents = ModuleType.query.get_parent()
    return render_template('admin/showmachine.html', parents=parents)


@admin.route("/addmachine/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def addmachine():
    form = AddMachineForm()
    if form.validate_on_submit():
        machine = Machine()
        form.populate_obj(machine)
        db.session.add(machine)
        db.session.commit()
        flash(_(u"Add {0} successfully!".format(machine.name)), "success")
        return redirect(url_for("admin.showmachine"))
    parents = ModuleType.query.get_parent()
    return render_template('admin/addmachine.html', form=form, parents=parents)


@admin.route("/<int:machine_id>/delmachine/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def delmachine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    db.session.delete(machine)
    db.session.commit()

    flash(_(u"{0} has been deleted".format(machine.name)), "success")
    return redirect(url_for("admin.showmachine"))


@admin.route("/<int:machine_id>/editmachine/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def editmachine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    form = EditMachineForm(machine)
    if form.validate_on_submit():
        machine.m_update_time = datetime.now()
        form.populate_obj(machine)
        db.session.commit()
        flash(_(u"Update {0} informatiion successfully".format(machine.name)),
              "success")
        return redirect(url_for("admin.showmachine"))
    parents = ModuleType.query.get_parent()
    return render_template('admin/editmachine.html', form=form,
                           parents=parents)

'''
@admin.route("/<int:machine_id>/singlemachine/")
@adm.require(401)
def singlemachine(machine_id):
    parents = ModuleType.query.get_parent()

    return render_template('admin/singlemachine.html', machine_id=machine_id, parents=parents)


@admin.route("/<int:machine_id>/singlemachine_sec10/")
@adm.require(401)
def singlemachine_sec10(machine_id):
    parents = ModuleType.query.get_parent()
    return render_template('admin/singlemachine_sec10.html', machine_id=machine_id, parents=parents)


@admin.route("/<int:machine_id>/singlemachine_hour/")
@adm.require(401)
def singlemachine_hour(machine_id):
    parents = ModuleType.query.get_parent()
    return render_template('admin/singlemachine_hour.html', machine_id=machine_id, parents=parents)
'''


@admin.route("/showmodule/")
@auth.require(401)
@adm.require(401)
def showmodule():
    parents = ModuleType.query.get_parent()
    return render_template('admin/showmodule.html', parents=parents)


@admin.route("/addmodule/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def addmodule():
    form = AddModuleForm()
    choices = [(item.id, _(item.name))
               for item in ModuleType.query.get_parent()]
    choices.append((0, _("parent")))
    form.parent_id.choices = choices
    if form.validate_on_submit():
        module = ModuleType()
        form.populate_obj(module)
        db.session.add(module)
        db.session.commit()
        flash(_(u"Add {0} successfully!".format(module.name)), "success")
        return redirect(url_for("admin.showmodule"))
    parents = ModuleType.query.get_parent()
    return render_template('admin/module.html', form=form, parents=parents)


@admin.route("/<int:module_id>/delmodule/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def delmodule(module_id):
    module = ModuleType.query.get_or_404(module_id)
    if module.parent_id == 0:
        sub_modules = ModuleType.query.\
            getsubmodule_by_parentid(module.id).all()
        if sub_modules:
            for item in sub_modules:
                db.session.delete(item)
    db.session.delete(module)
    db.session.commit()

    flash(_(u"{0} has been deleted".format(module.name)), "success")

    return redirect(url_for("admin.showmodule"))


@admin.route("/<int:module_id>/editmodule/", methods=("GET", "POST"))
@auth.require(401)
@adm.require(401)
def editmodule(module_id):
    module = ModuleType.query.get_or_404(module_id)
    form = EditModuleForm(module)
    if module.parent_id:
        choices = [(item.id, _(item.name))
                   for item in ModuleType.query.get_parent()]
        choices.append((0, _("parent")))
    else:
        choices = [(0, _("parent"))]
    form.parent_id.choices = choices
    if form.validate_on_submit():
        module.type_update_time = datetime.now()
        form.populate_obj(module)
        db.session.commit()
        flash(_(u"Update {0} informatiion successfully".format(module.name)),
              "success")
        return redirect(url_for("admin.showmodule"))
    parents = ModuleType.query.get_parent()
    return render_template('admin/module.html', form=form, parents=parents)
