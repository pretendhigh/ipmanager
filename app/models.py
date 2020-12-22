from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)    



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Ipinfo(SearchableMixin, db.Model):
    __searchable__ = ['ip', 'hostname', 'device_type', 'user', 'project']
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), index=True, unique=True)
    hostname = db.Column(db.String(64))
    device_type = db.Column(db.String(64))
    user = db.Column(db.String(64))
    project = db.Column(db.String(128))
   
    def __repr__(self):
        return '<Ip {}>'.format(self.ip)

db.event.listen(db.session, 'before_commit', Ipinfo.before_commit)
db.event.listen(db.session, 'after_commit', Ipinfo.after_commit)


