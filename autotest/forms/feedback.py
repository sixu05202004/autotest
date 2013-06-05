# -*- coding: utf-8 -*-
"""
    feedback.py
    ~~~~~~~~~~~

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, TextField, required, TextAreaField, SelectField
from flask.ext.babel import lazy_gettext as _
from .validators import is_legal_name


class AddQuestionForm(Form):

    description = TextAreaField(_(u"问题描述"))

    submit = SubmitField(_(u"提交"))
