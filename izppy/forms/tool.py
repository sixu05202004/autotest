#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    tool.py
    ~~~~~~~~~~~

    pmc ulc form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, TextField, TextAreaField,\
    SelectField, required, HiddenField
from flask.ext.babel import lazy_gettext as _

context_default = u"""88-0.1&127-0.05^美容院-0.01&美容-0.1&汽车-0.2&假日-0.1&手机-0.15&自行车-0.16&电脑-0.21"""
ulc_cate_default = u"2565:0.960877,3330:0.022358,4612:0.006409,1025:0.016769,1030:0.003587"
policy_default = u"WP178690114"


class PmcForm(Form):
    next = HiddenField()
    host = TextField(_(u"Redis Host:"), default="127.0.0.1", validators=[
        required(message=_(u"Host 不能为空！"))])
    port = TextField(_(u"Redis Port:"), default="6379", validators=[
        required(message=_(u"Port 不能为空！"))])

    db = SelectField(_(u"Redis db:"), coerce=int, choices=[(8, _(u'redis_url(8)'))])

    password = TextField(_(u"Redis Password:"))
    url = TextField(_(u"Url\Refer(正常情况下请不要输入http://):"),
                    default=u"www.hao123.com",
                    validators=[required(message=_(u"Url 不能为空！"))])

    context = TextAreaField(_(u"context:"), default=context_default)
    submit = SubmitField(_(u"生成"))


class UlcCookieForm(Form):
    next = HiddenField()
    host = TextField(_(u"Redis Host:"), default="127.0.0.1", validators=[
        required(message=_(u"Host 不能为空！"))])
    port = TextField(_(u"Redis Port:"), default="6379", validators=[
        required(message=_(u"Port 不能为空！"))])
    password = TextField(_(u"Redis Password:"))
    cookie = TextField(_(u"Cookie:(16 进制.当流量来源为非IDCLICK的时候,cookie的值为tid的值)"), default=u"A0FD935395DDFC53", validators=[
        required(message=_(u"Cookie 不能为空！"))])
    type = SelectField(_(u"流量来源:"), choices=[('310000', 'IDCLICK'), ('320000', 'TANX'), ('330000', 'GOOGLE')])
    udc_cate = TextAreaField(_(u"udc_cate:"), default=ulc_cate_default)
    policy = TextAreaField(_(u"policy(term):(如WP121;WP234;HP456;text;test 表示121,234,456三种策略ID以及btc的关键字 text和test)"), default=policy_default)
    submit = SubmitField(_(u"生成"))


class UlcIPUAForm(Form):
    next = HiddenField()
    host = TextField(_(u"Redis Host:"), default="127.0.0.1", validators=[
        required(message=_(u"Host 不能为空！"))])
    port = TextField(_(u"Redis Port:"), default="6379", validators=[
        required(message=_(u"Port 不能为空！"))])
    password = TextField(_(u"Redis Password:"))

    ip = TextField(_(u"IP:(暂支持北京地区 IP)"), default=u"10.0.35.100", validators=[
        required(message=_(u"IP 不能为空！"))])
    ua = TextAreaField(_(u"UA:(如:Mozilla/5.0 (Windows NT 6.1; WOW64))"),
                       default=u"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0", validators=[
                       required(message=_(u"UA 不能为空！"))])
    udc_cate = TextAreaField(_(u"udc_cate:"), default=ulc_cate_default)
    policy = TextAreaField(_(u"policy(term):(如WP121;WP234;HP456;text;test 表示121,234,456三种策略ID以及btc的关键字 text和test)"), default=policy_default)
    submit = SubmitField(_(u"生成"))
