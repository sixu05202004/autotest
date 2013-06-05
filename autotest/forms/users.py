# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~~~~~~

    login,singup,password form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""


from flask.ext.wtf import Form, HiddenField, BooleanField, PasswordField,\
    SubmitField, TextField, required, email, equal_to, ValidationError, \
    RadioField
from flask.ext.babel import gettext, lazy_gettext as _
from autotest.extensions import db
from autotest.models.users import User
from .validators import is_legal_name


class LoginForm(Form):

    next = HiddenField()

    remember = BooleanField(_(u"记住我"))

    login = TextField(_(u"用户名(邮箱地址):"), validators=[
                      required(message=
                               _(u"请输入用户名或者邮箱地址"))])

    password = PasswordField(_(u"密码:"), validators=[
                             required(message=
                                      _(u"请输入密码"))])

    submit = SubmitField(_(u"登陆"))


class SignupForm(Form):

    next = HiddenField()

    username = TextField(_(u"用户名:"), validators=[
                         required(message=_(u"请输入用户名或者邮箱地址")),
                         is_legal_name])

    password = PasswordField(_(u"密码:"), validators=[
                             required(message=_(u"请输入密码"))])

    password_again = PasswordField(_(u"确认密码:"), validators=[
                                   equal_to("password", message=
                                            _(u"密码不一致"))])

    email = TextField(_(u"邮箱地址:"), validators=[
                      required(message=_(u"请输入邮箱地址")),
                      email(message=_(u"请输入有效的邮箱地址"))])

    submit = SubmitField(_(u"注册"))

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError(gettext(u"用户名已经存在"))

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError(gettext(u"邮箱地址已经存在"))


class EditAccountForm(Form):

    username = TextField(_(u"用户名:"), validators=[
                         required(_(u"请输入用户名")), is_legal_name])

    email = TextField(_(u"邮箱地址:"), validators=[
                      required(message=_(u"请输入邮箱地址")),
                      email(message=_(u"请输入有效的邮箱地址"))])

    email_alerts = BooleanField(_(u"开启邮件提醒"))

    status = BooleanField(_(u"账号状态"))

    role = RadioField(_(u"角色"), default=User.MEMBER, coerce=int, choices=(
                      (User.MEMBER, _(u"普通用户")), (User.MODERATOR,
                      _(u"高级用户")), (User.ADMIN, _(u"管理员"))))

    submit = SubmitField(_(u"保存"))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditAccountForm, self).__init__(*args, **kwargs)

    def validate_username(self, field):
        user = User.query.filter(db.and_(
                                 User.username.like(field.data),
                                 db.not_(User.id == self.user.id))).first()

        if user:
            raise ValidationError(gettext(u"用户名已经存在"))

    def validate_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id == self.user.id))).first()
        if user:
            raise ValidationError(gettext(u"邮箱地址已经存在"))


class ChangePasswordForm(Form):

    password = PasswordField(_(u"密码:"), validators=[
                             required(message=_(u"请输入密码"))])

    password_again = PasswordField(_(u"确认密码:"), validators=[
                                   equal_to("password", message=
                                            _(u"密码不一致"))])

    submit = SubmitField(_(u"保存"))


class EditMyAccountForm(Form):

    username = TextField(_(u"用户名:"), validators=[
                         required(_(u"请输入用户名")), is_legal_name])

    email = TextField(_(u"邮箱地址:"), validators=[
                      required(message=_(u"请输入邮箱地址")),
                      email(message=_(u"请输入有效的邮箱地址"))])

    email_alerts = BooleanField(_(u"开启邮件提醒"))

    status = BooleanField(_(u"账号状态"))

    submit = SubmitField(_(u"保存"))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditMyAccountForm, self).__init__(*args, **kwargs)

    def validate_username(self, field):
        user = User.query.filter(db.and_(
                                 User.username.like(field.data),
                                 db.not_(User.id == self.user.id))).first()

        if user:
            raise ValidationError(gettext(u"用户名已经存在"))

    def validate_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id == self.user.id))).first()
        if user:
            raise ValidationError(gettext(u"邮箱地址已经存在"))
