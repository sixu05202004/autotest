# -*- coding: utf-8 -*-
"""
    feedback.py
    ~~~~~~~~~~~

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, TextAreaField
from flask.ext.babel import lazy_gettext as _


class AddQuestionForm(Form):

    description = TextAreaField(_(u"问题描述"))

    submit = SubmitField(_(u"提交"))
