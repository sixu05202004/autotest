#-*- coding: utf-8 -*-
"""
    about.py
    ~~~~~~~~~

    about views: about manage

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, flash, redirect, url_for, render_template, g
from izppy.forms import AddQuestionForm
from izppy.models.feedback import FeedBack
from izppy.extensions import db
from izppy.permissions import auth
#from flask.ext.babel import lazy_gettext as _

about = Module(__name__)


@about.route("/showquestions/")
@auth.require(401)
def showquestion(page=1):
    question = FeedBack.query.getall().all()
    return render_template('showqustions.html', question=question)


@about.route("/feedback/", methods=("GET", "POST"))
@auth.require(401)
def feedback():
    print unicode(g.user)
    form = AddQuestionForm()
    if form.validate_on_submit():
        feedback = FeedBack()
        feedback.name = g.user.username
        feedback.email = g.user.email
        form.populate_obj(feedback)
        db.session.add(feedback)
        db.session.commit()
        db.session.remove()
        flash(u"Add {0} successfully!".format(feedback.name), "success")
        return redirect(url_for('index.index'))
    question = FeedBack.query.getall().all()
    return render_template('/about/feedback.html', form=form, question=question)


@about.route("/release/")
@auth.require(401)
def release():
    return render_template('about/release.html')


@about.route("/chartdirector/")
@auth.require(401)
def chartdirector():
    return render_template('about/chartdirector.html')
'''
@about.route("/test_pmc.html/")
def chartdirector():
    return render_template('about/test_pmc.html')
'''


@about.route("/test/")
def test():
    return render_template("errors/404.html")