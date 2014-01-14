import sys
sys.path.append('D:\svn\\test\\src\\neptune\\v3r1\\izppy')

from izppy.models import User, Case, ModuleType
from izppy.extensions import db
from flask.ext.testing import unittest
from tests import TestCase


class test_user(TestCase):
    def test_admin(self):
    	a=ModuleType(name=u'aaa')
    	b=ModuleType(parent_id=1, name=u'baa')
    	c=ModuleType(name=u'aaa11')

    	db.session.add(a)
    	db.session.add(b)
    	db.session.add(c)
    	db.session.commit()
    	print ModuleType.query.get_allsubmodule().all()
    	print ModuleType.query.get_by_parent_id(1).all()


if __name__ == '__main__':
    unittest.main()
