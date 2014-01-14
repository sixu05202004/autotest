# -*- coding: utf-8 -*-
#Please change sys.apth
import sys
sys.path.append('D:\\v3r11\izppy')

from izppy.forms import LoginForm, ChangePasswordForm, SignupForm, EditAccountForm
from flask.ext.testing import unittest
from tests import TestCase
from izppy.models.users import User
from izppy.extensions import db


class TestUser(TestCase):
    def setUp(self):
        super(TestUser, self).setUp()

        self.user = User(username=u"tester",
                         email=u"tester@example.com",
                         password=u"testing")

        db.session.add(self.user)
        db.session.commit()

    def test_login1(self):
        form = LoginForm(password="testing")
        #form1 = SignupForm(username= u"tester1", password= u"testing",password_again=u"testing",email=u"teser@example.com", submit = "True")
        #form2 = EditAccountForm(username=u"tester", email = u"tester@example.com", submit = "True")
        #form3 = ChangePasswordForm(password = u"test1ing", password_again = u"test1ing", submit= "True")
        form.validate()
        assert form.errors.get("login") == ['Need an email or username']

    def test_login2(self):
        form = LoginForm()
        form.validate()
        assert form.errors.get("login") == ['Need an email or username']
        assert form.errors.get("password") == ['Need a password']

    def test_login3(self):
        form = LoginForm(login="aa")
        form.validate()
        assert form.errors.get("password") == ['Need a password']

    def test_login4(self):
        form = LoginForm(login="aa", password="aa")
        self.assertEqual(form.validate(), False)

    def test_login5(self):
        form = LoginForm(login="tester", password="aa")
        self.assertEqual(form.validate(), False)

    def test_login6(self):
        form = LoginForm(login=u"tester", password=u"testing", submit=True)
        print dir(form)
        print form.validate()
        self.assertEqual(form.validate(), True)


if __name__ == '__main__':
    unittest.main()
