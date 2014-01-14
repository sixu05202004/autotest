"""
    feedback.py
    ~~~~~~~~~~~

    feedback table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime
#from werkzeug import cached_property
from flask.ext.sqlalchemy import BaseQuery
from izppy.extensions import db


class FeedBackQuery(BaseQuery):
    def getall(self):
        return self.order_by(FeedBack.id.desc())

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(FeedBack.description.ilike(keyword))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()


class FeedBack(db.Model):
    __tablename__ = "FeedBack"
    query_class = FeedBackQuery
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(200), nullable=False)
    email = db.Column(db.Unicode(200), nullable=False)
    description = db.Column(db.UnicodeText)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(FeedBack, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<%s>" % self
