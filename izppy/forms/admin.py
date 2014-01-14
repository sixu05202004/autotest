# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~

    module,code,machine form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, RadioField,\
    SelectField, TextField, required, ValidationError, \
    TextAreaField
from flask.ext.babel import gettext, lazy_gettext as _
from izppy.models.admin import ModuleType, Machine
from izppy.extensions import db
from .validators import is_legal_name


class AddModuleForm(Form):
    '''It is used for adding modules, defines add modules form.'''

    name = TextField(_(u"模块名:"), validators=[
        required(message=_(u"请输入模块名称")), is_legal_name])

    description = TextAreaField(_(u"描述:"))

    parent_id = SelectField(_(u"所属模块:"), default=0,
                            coerce=int)
    input_template = TextAreaField(_(u"输入用例模板:"))

    output_template = TextAreaField(_(u"输出用例模板:"))

    submit = SubmitField(_(u"提交"))

    def validate_name(self, field):

        moduletype = ModuleType.query.filter(
            ModuleType.name.like(field.data)).first()
        if moduletype:
            raise ValidationError(gettext(u"模块名已经存在"))


class EditModuleForm(Form):
    '''It is used for editing modules, defines edit modules form.'''

    name = TextField(_(u"模块名:"), validators=[
        required(_(u"请输入模块名称")), is_legal_name])

    description = TextAreaField(_(u"描述:"))

    parent_id = SelectField(_(u"所属模块:"), default=0,
                            coerce=int)

    input_template = TextAreaField(_(u"输入用例模板:"))

    output_template = TextAreaField(_(u"输出用例模板:"))

    submit = SubmitField(_(u"保存"))

    def __init__(self, moduleType, *args, **kwargs):
        self.moduleType = moduleType
        kwargs['obj'] = self.moduleType
        super(EditModuleForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        moduleType = ModuleType.query.filter(db.and_(
                                             ModuleType.name.like(field.data),
                                             db.not_(ModuleType.id == self.moduleType.id))).first()
        if moduleType:
            raise ValidationError(gettext(u"模块名已经存在"))


class AddMachineForm(Form):
    '''It is used for adding machines, defines add machines form.'''

    name = TextField(_(u"机器名:"), validators=[
        required(_(u"请输入机器名")), is_legal_name])
    description = TextAreaField(_(u"描述:"))
    status = RadioField(_(u"状态:"), default=Machine.OK, coerce=int, choices=((
        Machine.OK, _(u"正常")), (Machine.REALLY, _(u"停用"))))
    username = TextField(_(u"用户名:"))
    password = TextField(_(u"密码:"))
    url_hudson = TextField(_(u"Hudson地址:"))
    submit = SubmitField(_(u"提交"))

    def validate_name(self, field):
        machine = Machine.query.filter(
            Machine.name.like(field.data)).first()
        if machine:
            raise ValidationError(gettext(u"机器名已经存在"))


class EditMachineForm(Form):
    '''It is used for editing machines, defines edit machines form.'''

    name = TextField(_(u"机器名:"), validators=[
        required(_(u"请输入机器名")), is_legal_name])
    description = TextAreaField(_(u"描述:"))
    status = RadioField(_(u"状态:"), default=Machine.OK, coerce=int, choices=((
        Machine.OK, _(u"正常")), (Machine.REALLY, _(u"停用"))))
    username = TextField(_(u"用户名:"))
    password = TextField(_(u"密码:"))
    url_hudson = TextField(_(u"Hudson地址:"))
    key = TextField(_(u"SSH Key:"))
    submit = SubmitField(_(u"保存"))

    def __init__(self, machine, *args, **kwargs):
        self.machine = machine
        kwargs['obj'] = self.machine
        super(EditMachineForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        machine = Machine.query.filter(db.and_(
                                       Machine.name.like(field.data),
                                       db.not_(Machine.id == self.machine.id))).first()
        if machine:
            raise ValidationError(gettext(u"机器名已经存在"))
