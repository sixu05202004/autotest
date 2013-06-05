"""
    task.py
    ~~~~~~~~~~~

    task table structure and query function.

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime
from werkzeug import cached_property
from sqlalchemy import event, DDL
from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import Permission, UserNeed
from autotest.permissions import moderator
from autotest.models.cases import Case
from autotest.models.admin import ModuleType
from autotest.models.codes import Code
from autotest.models.users import User
from autotest.extensions import db
from autotest.helpers import get_access, get_hudson

task_case = db.Table('task_case',
                     db.Column('cases_id', db.Integer, db.ForeignKey('cases.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                     )
task_code = db.Table('task_code',
                     db.Column('code_id', db.Integer, db.ForeignKey('code.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                     )
"""
task_machine = db.Table('task_machine',
                        db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')),
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)
"""


class TaskQuery(BaseQuery):

    def jsonify(self):
        for task in self.all():
            yield task.json

    def getall(self):
        return self.all()

    def get_by_name(self, name):
        return self.filter(Task.name == name).first()

    def private_count(self, user=None):
        criteria = []
        if user:
            criteria.append(Task.author_id == user.id)
            criteria.append(Task.access == Task.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def public_count(self, user=None):
        criteria = []
        if user:
            criteria.append(Task.author_id == user.id)
            criteria.append(Task.access == Task.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def public(self, user=None):
        if user and user.is_moderator:
            return self.order_by(Task.id.desc())
        return self.filter(Task.access == Task.PUBLIC).order_by(Task.id.desc())

    def private(self, user=None):
        if user and user.is_moderator:
            return self.order_by(Task.id.desc())
        criteria = []
        if user:
            criteria.append(Task.author_id == user.id)
            criteria.append(Task.access == Task.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def get_by_id(self, id):
        return self.get(id)

    def getall_by_authorid(self, id):
        return self.filter(Task.author_id == id).order_by(Task.id.desc())

    def getall_by_excute_times(self, times):
        return self.filter(Task.task_excute_times == times).order_by(Task.id.desc())

    def getpublic_by_moudletype(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Task.moduletype_id == id).order_by(Task.id.desc())
        criteria = [Task.moduletype_id == id]
        criteria.append(Task.access == Task.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def getprivate_by_moudletype(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Task.moduletype_id == id).order_by(Task.id.desc())
        criteria = [Task.moduletype_id == id]
        if user:
            criteria.append(Task.author_id == user.id)
            criteria.append(Task.access == Task.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def getpublic_by_parentid(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Task.parent_id == id).order_by(Task.id.desc())
        criteria = [Task.parent_id == id]
        criteria.append(Task.access == Task.PUBLIC)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def getprivate_by_parentid(self, id, user=None):
        if user and user.is_moderator:
            return self.filter(Task.parent_id == id).order_by(Task.id.desc())
        criteria = [Task.parent_id == id]
        if user:
            criteria.append(Task.author_id == user.id)
            criteria.append(Task.access == Task.PRIVATE)
        return self.filter(reduce(db.and_, criteria)).order_by(Task.id.desc())

    def restricted_search(self, user=None):
        if user and user.is_moderator:
            return self
        criteria = [Task.access == Task.PUBLIC]
        if user:
            criteria.append(Task.author_id == user.id)
        return self.filter(reduce(db.or_, criteria)).order_by(Task.id.desc())

    def search(self, keywords, user=None):
        criteria = []
        if user.is_moderator:
            for keyword in keywords.split():
                keyword = '%' + keyword + '%'
                criteria.append(db.or_(Task.name.ilike(keyword),
                                Task.description.ilike(keyword),
                                Task.id.ilike(keyword)))
        else:
            for keyword in keywords.split():
                keyword = '%' + keyword + '%'
                criteria.append(db.or_(db.and_(db.or_(Task.name.ilike(keyword),
                                                      Task.description.ilike(keyword),
                                                      Task.id.ilike(keyword)),
                                               Task.access == Task.PUBLIC),
                                       db.and_(db.or_(Task.name.ilike(keyword),
                                                      Task.description.ilike(keyword),
                                                      Task.id.ilike(keyword)),
                                               Task.author_id == user.id)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct().order_by(Task.id.desc())


class Task(db.Model):
    __tablename__ = "task"
    query_class = TaskQuery
    PUBLIC = 100
    PRIVATE = 300
    PER_PAGE = 20
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=True)
    moduletype_id = db.Column(db.Integer,
                              db.ForeignKey(ModuleType.id, ondelete='CASCADE'),
                              nullable=True)
    parent_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Unicode(200), unique=True, nullable=False)
    case = db.relationship("Case", secondary="task_case", backref=db.backref("task", lazy='dynamic'))
    code = db.relationship("Code", secondary="task_code", backref=db.backref("task", lazy='dynamic'))
    # machine_id = db.Column(db.Integer,db.ForeignKey(Machine.id, ondelete='CASCADE'),nullable=False)
    access = db.Column(db.Integer, default=PUBLIC)
    hudson = db.Column(db.Integer, default=None)
    task_excute_times = db.Column(db.Integer, default=0)
    description = db.Column(db.UnicodeText)
    command = db.Column(db.UnicodeText, nullable=False)
    runtime = db.Column(db.UnicodeText)
    timing = db.Column(db.UnicodeText, default=0)
    svn = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.UnicodeText, nullable=False)
    email_topic = db.Column(db.UnicodeText, nullable=False)
    other = db.Column(db.UnicodeText)
    task_create_time = db.Column(db.DateTime, default=datetime.now)
    task_update_time = db.Column(db.DateTime, default=datetime.now)
    author = db.relation(User, innerjoin=True, lazy="joined")
    moduletype = db.relation(ModuleType, innerjoin=True, lazy="joined")
    # machine = db.relation(Machine, innerjoin=True, lazy="joined")

    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def default(self):
            return Permission(UserNeed(self.obj.author_id)) & moderator

        @cached_property
        def view(self):
            if self.obj.access == Task.PUBLIC:
                return Permission()
            return self.default

        @cached_property
        def run(self):
            if self.obj.access == Task.PUBLIC:
                return Permission()
            return self.default

        @cached_property
        def edit(self):
            return self.default

        @cached_property
        def delete(self):
            return self.default

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.access = self.access or self.PUBLIC

    @staticmethod
    def count_task(self):
        print self.task

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def attach_task_url(self):
        result = []
        if self.task_path:
            result = self.task_path.split(";").remove('')
        return result

    @cached_property
    def attach_code_url(self):
        result = []
        if self.code_path:
            result = self.code_path.split(";").remove('')
        return result

    @cached_property
    def attach_other_url(self):
        result = []
        if self.other_path:
            result = self.other_path.split(";").remove('')
        return result

    @cached_property
    def json(self):
        return dict(id=self.id,
                    author=self.author.username,
                    name=self.name,
                    description=self.description,
                    hudson=get_hudson(self.hudson),
                    times=self.task_excute_times,
                    command=self.command,
                    runtime=self.runtime,
                    timing=self.timing,
                    svn=self.svn,
                    email=self.email,
                    email_topic=self.email_topic,
                    other=self.other,
                    case=str([i.title for i in self.case]),
                    code=str([i.name for i in self.code]),
                    task_create_time=str(self.task_create_time),
                    task_update_time=str(self.task_update_time),
                    access=get_access(self.access),
                    tasktype=self.moduletype.name)


class TaskcountQuery(BaseQuery):

    def jsonify(self):
        for taskcount in self.all():
            yield taskcount.json

    def getall(self):
        return self.order_by(Taskcount.id.desc())

    def get_all_pass(self):
        return self.filter(Taskcount.result == Taskcount.PASS)

    def get_all_fail(self):
        return self.filter(Taskcount.result == Taskcount.FAIL)

    def data(self, id):
        return self.filter(Taskcount.task_id == id).order_by(Taskcount.build_id.desc())

    def get_task_next(self, id):
        criteria = [Taskcount.task_id == id]
        criteria.append(Taskcount.next == 1)
        return self.filter(reduce(db.and_, criteria)).first()

    def get_task_build(self, task_id, build_id):
        criteria = [Taskcount.task_id == task_id]
        criteria.append(Taskcount.build_id == build_id)
        return self.filter(reduce(db.and_, criteria)).first()

    def get_case_all(self, id):
        return db.engine.execute("select count(*)  from  task_case where task_id=%s"
                                 % (id)).fetchall()[0][0]


class Taskcount(db.Model):
    PASS = 0
    FAIL = 1
    PER_PAGE = 20
    __tablename__ = "task_count"
    query_class = TaskcountQuery
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id, ondelete='CASCADE'), nullable=False)
    case_all = db.Column(db.Integer)
    case_pass = db.Column(db.Integer)
    case_fail = db.Column(db.Integer)
    result = db.Column(db.Integer, default=0)
    result_path = db.Column(db.String(150))
    fail_case = db.Column(db.UnicodeText)
    start_time = db.Column(db.DateTime, default=datetime.now)
    stop_time = db.Column(db.DateTime, default=datetime.now)
    timing = db.Column(db.UnicodeText,default=0)
    other = db.Column(db.UnicodeText)
    build_id = db.Column(db.Integer)
    next = db.Column(db.Integer, default=0, nullable=False)
    task = db.relation(Task, innerjoin=True, lazy="joined")

    def __init__(self, *args, **kwargs):
        super(Taskcount, self).__init__(*args, **kwargs)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    task_id=self.task_id,
                    case_all=self.case_all,
                    case_pass=self.case_pass,
                    case_fail=self.case_fail,
                    result=self.result,
                    result_path=self.result_path,
                    fail_case=self.fail_case,
                    start_time=str(self.start_time),
                    stop_time=str(self.stop_time),
                    timing=self.timing,
                    build_id=self.build_id,
                    next=self.next,
                    other=self.other)

update_task_state = DDL('''
CREATE TRIGGER update_task_state AFTER INSERT ON task_count FOR EACH ROW
  BEGIN
    UPDATE task SET task_excute_times=task_excute_times+1 WHERE task.id = new.task_id;
  END;''')

update_task_state_delete = DDL('''
CREATE TRIGGER update_task_state_delete AFTER DELETE ON task_count FOR EACH ROW
  BEGIN
    UPDATE task SET task_excute_times=task_excute_times-1 WHERE (task.id = old.task_id) AND (task.task_excute_times>=1);
  END;''')
event.listen(Taskcount.__table__, 'after_create', update_task_state)
event.listen(Taskcount.__table__, 'after_create', update_task_state_delete)

'''
class TaskdetailQuery(BaseQuery):

    def jsonify(self):
        for taskdetail in self.all():
            yield taskdetail.json

    def getall(self):
        return self.order_by(Taskdetail.id.desc())

class Taskdetail(db.Model):
    PASS = 0
    FAIL = 1
    __tablename__ = "task_detail"
    query_class = TaskdetailQuery
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id, ondelete='CASCADE'), nullable=False)
    build_id = db.Column(db.Integer)
    case_id = db.Column(db.Integer)
    case_result = db.Column(db.Integer)
    case_log = db.Column(db.UnicodeText)
    def __init__(self, *args, **kwargs):
        super(Taskdetail, self).__init__(*args, **kwargs)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    task_id=self.id,
                    build_id=self.build_id,
                    case_id=self.case_id,
                    case_result=self.case_result,
                    case_log=self.case_log)
'''
