# -*- coding: utf-8 -*-

#please change it to yours path!!!!
import sys
sys.path.append('D:\svn\\test\\src\\neptune\\v3r1\\izppy')

from flask.ext.principal import Permission, UserNeed
from izppy.models import User, Case
from izppy.extensions import db
from flask.ext.testing import unittest
from izppy.permissions import moderator
from tests import TestCase


class test_user(TestCase):
    def test_add_user(self):
        user = User(username=u"tester", email="tester@example.com", password="test")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

    def test_authenticate_user1(self):
        user = User(username=u"tester", email="tester@example.com", password="test")
        db.session.add(user)
        db.session.commit()
        assert User.query.authenticate("tester", "test") == (user, True)

    def test_authenticate_user2(self):
        user = User(username=u"tester", email="tester@example.com", password="test")
        db.session.add(user)
        db.session.commit()

        assert User.query.authenticate("tester@example.com", "test") == (user, True)

    def test_authenticate_user3(self):
        user = User(username=u"tester", email="tester@example.com", password="test")
        db.session.add(user)
        db.session.commit()
        assert User.query.authenticate("tester@example.com", "tes11t") == (user, True)

    def test_authenticate_user4(self):
        user = User(username=u"tester", email="tester@example.com", password="test")
        db.session.add(user)
        db.session.commit()
        assert User.query.authenticate("tester1@example.com", "test") == (user, True)

    def test_for_case(self):
        case = Case(author_id=1, case_type=2)
        db.session.add(case)
        db.session.commit()
        assert case.access == 100
        assert case.permissions.view == Permission()


if __name__ == '__main__':
    unittest.main()
