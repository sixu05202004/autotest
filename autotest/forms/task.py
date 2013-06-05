# -*- coding: utf-8 -*-
"""
    task.py
    ~~~~~~~~~~~

    task form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, SelectField,\
    TextField, required, FileField, RadioField, ValidationError,\
    SelectMultipleField, FieldList, TextAreaField, validators
from wtforms import widgets
from flask.ext.babel import gettext, lazy_gettext as _
#from flask.ext.uploads import UploadSet
from .validators import is_legal_taskname, is_legal_svn
from autotest.extensions import db
from autotest.models import Task


class AddTaskForm(Form):

    name = TextField(_(u"任务名称"), validators=[
        required(message=_(u"任务名称不为空")), is_legal_taskname])
    description = TextAreaField(_(u"描述"))
    access = RadioField(_(u"状态"), default=Task.PUBLIC, coerce=int,
                        choices=((Task.PUBLIC, _(u"公开")),
                       (Task.PRIVATE, _(u"私有"))))

    moduletype_id = SelectField(_(u"选择模块"), coerce=int)

    case_list = SelectMultipleField(_(u"选择用例"), coerce=int, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    code_list = SelectMultipleField(_(u"选择代码"), coerce=int, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    command = TextAreaField(_(u"执行命令"), default = u"hg clone http://10.0.2.205:9090/hg/test.cgi/script/\n./script/command.sh")

    runtime = TextAreaField(_(u"运行时间"))

    svn = TextAreaField(_(u"svn地址"), validators=[is_legal_svn])

    email = TextAreaField(_(u"邮箱地址"))

    email_topic = TextAreaField(_(u"邮件主题"))

    other = TextAreaField(_(u"其他"))

    submit = SubmitField(_(u"添加"))

    def validate_name(self, field):
        task = Task.query.filter(Task.name.like(field.data)).first()
        if task:
            raise ValidationError(gettext(u"该名称已经被使用"))


class EditTaskForm(Form):
    name = TextField(_(u"任务名称"), validators=[
        required(message=_(u"任务名称不为空")), is_legal_taskname])
    description = TextAreaField(_(u"描述"))
    access = RadioField(_(u"状态"), default=Task.PUBLIC, coerce=int,
                        choices=((Task.PUBLIC, _(u"公开")),
                       (Task.PRIVATE, _(u"私有"))))

    moduletype_id = SelectField(_(u"选择模块"), coerce=int)

    case_list = SelectMultipleField(_(u"选择用例"), coerce=int, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    code_list = SelectMultipleField(_(u"选择代码"), coerce=int, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    command = TextAreaField(_(u"执行命令"))

    runtime = TextAreaField(_(u"运行时间"))

    svn = TextAreaField(_(u"svn地址"), validators=[is_legal_svn])

    email = TextAreaField(_(u"邮箱地址"))

    email_topic = TextAreaField(_(u"邮件主题"))
    other = TextAreaField(_(u"其他"))

    submit = SubmitField(_(u"保存"))

    def __init__(self, task, *args, **kwargs):
        self.task = task
        kwargs['obj'] = self.task
        super(EditTaskForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        task = Task.query.filter(db.and_(Task.name.like(field.data),
                                         db.not_(Task.id == self.task.id))).first()
        if task:
            raise ValidationError(gettext(u"名称已经被使用"))
