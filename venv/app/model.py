from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    privilege = db.Column(db.Boolean())
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer) # 0 - 4, Index 0 is for supervisor
    time = db.Column(db.Integer) # 0 - 23
    date = db.Column(db.String(32)) # MM-DD-YYYY, Not being used now
    week = db.Column(db.Integer) # 0 - 6
    open = db.Column(db.Boolean())
    user_id = db.Column(db.String(64))


class DateTimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer) # 0 - 4, Index 0 is for supervisor
    time = db.Column(db.Integer) # 0 - 23
    date = db.Column(db.String(32)) # MM-DD-YYYY
    open = db.Column(db.Boolean())
    user_id = db.Column(db.String(64))


class ScheduleRange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(16)) # MM/DD/YYYY
    end_date = db.Column(db.String(16)) # MM/DD/YYYY


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
