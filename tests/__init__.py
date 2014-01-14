# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~

"""
#please change it to yours path!!!!
import sys
sys.path.append('D:\\svn\\test\\src\\neptune\\v3r1\\izppy')


from flask.ext.testing import TestCase as Base, Twill
#from izppy.models import User
from izppy import setup_app
from izppy.extensions import db


class TestCase(Base):

    """
    Base TestClass for your application.
    """

    def create_app(self):
        app = setup_app()
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def login(self, **kwargs):
        pass

    def logout(self):
        pass