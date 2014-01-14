import sys
sys.path.append('D:\svn\\test\\src\\neptune\\v3r1\\izppy')

from izppy.models import User, Case, ModuleType, Code
from izppy.extensions import db
from flask.ext.testing import unittest
from tests import TestCase


class test_user(TestCase):
    def test_case(self):
        
        user = User(username=u"tester", email="tester@example.com",
                    password="test", role=200)
        db.session.add(user)
        user1 = User(username=u"teste1r", email="tester1@example.com",
                     password="test")
        user2 = User(username=u"teste1r1", email="tester11@example.com",
                     password="test")
        db.session.add(user1)
        db.session.add(user2)
        a = ModuleType(parent_id=1, name="1")
        db.session.add(a)
        b = ModuleType(parent_id=2, name="2")
        db.session.add(b)
        case1 = Case(title='1', author_id=1, module_type=1)
        case2 = Case(title='1-1', author_id=2, module_type=2, access=300)
        code = Code(name='1', related_module=1)
        code1 = Code(name='2', related_module=2)
        db.session.add(case1)
        db.session.add(case2)
        db.session.add(code)
        db.session.add(code1)
        db.session.commit()
        
        #print len(Case.query.getcase_by_moudletype(3).all())

        self.assertEquals(len(Case.query.getall_by_authorid(1).all()), 1)
        self.assertEquals(Case.query.getall_by_authorid(2).all()[0].title,
                          '1-1')
        self.assertEquals(len(Case.query.search('1').all()), 2)
        self.assertEquals(len(Case.query.restricted_search(user).all()), 2)
        self.assertEquals(len(Case.query.restricted_search(user1).all()), 2)
        self.assertEquals(len(Case.query.restricted_search(user2).all()), 1)
        

if __name__ == '__main__':
    unittest.main()
