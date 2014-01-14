# -*- coding: utf-8 -*-
"""
    codes.py
    ~~~~~~~~~~~

    case form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, FileField, SubmitField, HiddenField,\
    TextField, required, ValidationError, SelectField, TextAreaField
from flask.ext.babel import gettext, lazy_gettext as _
from izppy.extensions import db
from izppy.models.codes import Code
from .validators import is_legal_name


class AddCodeForm(Form):
    '''It is used for adding codes, defines add codes form.'''

    next = HiddenField()
    name = TextField(_(u"名称:"), validators=[
        required(message=_(u"请输入名称")), is_legal_name]
    )

    description = TextAreaField(_(u"描述:"))

    related_module = SelectField(_(u"所属模块:"), default=0,
                                 coerce=int)
    path = FileField(u"代码文件",
                     validators=[required(message=_(u"请选择文件"))])

    submit = SubmitField(_(u"提交"))

    def validate_name(self, field):
        code = Code.query.filter(Code.name.like(field.data)).first()
        if code:
            raise ValidationError(gettext(u"名称已经存在"))


class EditCodeForm(Form):
    '''It is used for editing codes, defines edit codes form.'''

    next = HiddenField()
    name = TextField(_(u"名称:"), validators=[
        required(_(u"请输入名称")), is_legal_name])

    description = TextAreaField(_(u"描述:"))

    related_module = SelectField(_(u"所属模块:"), default=0, coerce=int)

    path = FileField(u"代码文件",
                     validators=[required(message=_(u"请选择文件"))])

    submit = SubmitField(_(u"保存"))

    def __init__(self, code, *args, **kwargs):
        self.code = code
        kwargs['obj'] = self.code
        super(EditCodeForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        code = Code.query.filter(db.and_(
                                 Code.name.like(field.data),
                                 db.not_(Code.id == self.code.id))).first()
        if code:
            raise ValidationError(gettext(u"名称已经存在"))
