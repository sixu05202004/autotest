#-*- coding: utf-8 -*-
"""
    code.py
    ~~~~~~~~~

    code views:code manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, g, redirect, url_for, render_template, request
from izppy.forms import AddCodeForm, EditCodeForm
from izppy.models.codes import Code
from izppy.models.admin import ModuleType
from izppy.extensions import db, up
from flask.ext.babel import lazy_gettext as _
from izppy.permissions import auth
from datetime import datetime
from izppy.views.tool import clear_cache
import os
from izppy.config import defaultconfig

code = Module(__name__)


def upload_file(AddCodeForm):
    folder = str(g.user) + "/" + str(AddCodeForm.name.data)
    sys_path = defaultconfig().UPLOADED_FILES_DEST + folder
    os.system("mkdir -p " + sys_path)
    os.system("chmod 777 " + sys_path)
    print sys_path
    os.system("rm -rf " + sys_path + "/*")
    print "zhengwei"
    uploadfile = up.save(AddCodeForm.path.data, folder=folder)
    print uploadfile
    filename = uploadfile.split('/')[-1]
    print filename
    os.chdir(sys_path)
    os.system("mv " + filename + " izptest." + filename.rsplit('.', 1)[1])

    if filename.rsplit('.', 1)[1] in ["zip"]:
        cmd1 = "unzip izptest.zip"
    elif filename.rsplit('.', 1)[1] in ["tar"]:
        cmd1 = "tar -xf izptest.tar"
    os.system(cmd1)
    os.system("rm izptest." + filename.rsplit('.', 1)[1])
    os.system("mv * izptest/")
    os.chdir(sys_path + '/izptest')
    os.system("hg init")
    os.system("hg add *")
    os.system("hg commit -m 'add'")
    return "izptest"
    #return filename.split('.')[0]


@code.route("/showallcode/")
@auth.require(401)
def showcode():
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('code/showallcode.html', parents=parents, nodes=nodes)


@code.route("/<int:parent_id>/<int:module_id>/showcode/")
@auth.require(401)
def showcode_module(module_id, parent_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(parent_id)
    return render_template('code/showmodulecode.html', module_id=module_id,
                           parents=parents, nodes=nodes)


@code.route("/parent/<int:module_id>/showcode/")
@auth.require(401)
def showcode_parent(module_id):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.getsubmodule_by_parentid(module_id)
    return render_template('code/showparentcode.html', module_id=module_id,
                           parents=parents, nodes=nodes)
'''
@code.route("/codesearch/")
@code.route("/codesearch/<int:page>/")
@auth.require(401)
def codesearch(page=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    searchword = request.args.get('s', '')
    if not searchword:
        return redirect(url_for('code.showcode'))
    codes = Code.query.search(searchword).paginate(page, Code.PER_PAGE)
    page_url = lambda page: url_for('code.codesearch',
                                    page=page)
    return render_template('code/showcode.html', page_obj=codes,
                           page_url=page_url, parents=parents, nodes = nodes)
'''


@code.route("/showsingle/<int:id>/")
@auth.require(401)
def showsingle(id=1):
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    code = Code.query.get_or_404(id)
    return render_template('code/showsingle.html', code=code,
                           parents=parents, nodes=nodes)


@code.route("/addcode/", methods=("GET", "POST"))
@auth.require(401)
def addcode():
    form = AddCodeForm(next=request.referrer)
    form.related_module.choices = [(item.id, _(item.name))
                                   for item in ModuleType.query.
                                   get_allsubmodule()]
    if form.validate_on_submit():
        code = Code()
        try:
            if form.path.has_file():
                try:
                    filename = upload_file(form)
                except:
                    flash(u"错误的压缩文件内容，请重新上传", "error")
                    return redirect(url_for("code.addcode"))
            code.author_id = g.user.id
            form.populate_obj(code)
            code.path = unicode(defaultconfig().CODE_URL + str(g.user) + "/" + str(form.name.data) + "/" + filename)
            code.parent_id = ModuleType.query.get_or_404(form.related_module.data).parent_id
            db.session.add(code)
            db.session.commit()
            clear_cache()
            flash(u"Add {0} successfully!".format(code.name), "success")
            return redirect(form.next.data or url_for("code.showcode"))
        except:
            flash(u"错误的文件类型，只允许ZIP或TAR", "error")
            return redirect(url_for("code.addcode"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('code/code.html', form=form, parents=parents, nodes=nodes)


@code.route("/<int:code_id>/delcode/", methods=("GET", "POST"))
@auth.require(401)
def delcode(code_id):
    code = Code.query.get_or_404(code_id)
    code.permissions.delete.test(403)
    cmd = "rm -rf " + defaultconfig().UPLOADED_FILES_DEST + str(g.user) + "/" + str(code.name)
    os.system(cmd)
    db.session.delete(code)
    db.session.commit()
    clear_cache()
    flash(u"{0} has been deleted".format(code.name), "success")
    return redirect(request.referrer or url_for("code.showcode"))


@code.route("/<int:code_id>/editcode/", methods=("GET", "POST"))
@auth.require(401)
def editcode(code_id):
    code = Code.query.get_or_404(code_id)
    code.permissions.edit.test(403)
    form = EditCodeForm(code, next=request.referrer)
    form.related_module.choices = [(item.id, _(item.name))
                                   for item in ModuleType.query.
                                   get_allsubmodule()]
    if form.validate_on_submit():
        if form.path.has_file():
            filename = up.save(form.path.data)
            print filename
            code.path = unicode(filename, "gbk")
            print code.path + "/n"
        code.code_update_time = datetime.now()
        code.parent_id = ModuleType.query.get_or_404(form.related_module.data).parent_id
        form.populate_obj(code)
        if code.parent_id != ModuleType.query.\
                get_or_404(form.related_module.data).parent_id:
            code.parent_id = ModuleType.query.\
                get_or_404(form.related_module.data).parent_id
        code.code_update_time = datetime.now()
        code.code_update_time = datetime.now()
        code.parent_id = ModuleType.query.get_or_404(form.related_module.data).parent_id
        db.session.add(code)
        db.session.commit()
        clear_cache()
        flash(u"Update {0} informatiion successfully".format(code.name),
              "success")
        return redirect(form.next.data or url_for("code.showcode"))
    parents = ModuleType.query.get_parent()
    nodes = ModuleType.query.get_allsubmodule()
    return render_template('code/code.html', form=form, parents=parents,
                           nodes=nodes)
