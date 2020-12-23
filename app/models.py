from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app import login, db
from flask import current_app
from flask_login import current_user, login_required
from flask_table import Table, Col
from time import time
import jwt


association_table = db.Table('association_table', 
    db.Column("contacts_id", db.Integer, db.ForeignKey("contact.id")),
    db.Column("groups_id", db.Integer, db.ForeignKey("group.id")))


@login.user_loader
def load_user(id):
    return user.query.get(int(id))



class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    skype_id = db.Column(db.String(64), index = True, unique = True)
    skype_name = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index = True, unique = True)
    contacts = db.relationship("contact", backref='user', lazy='dynamic')
    messages = db.relationship("message", backref='user', lazy ='dynamic')
    groups = db.relationship("group", backref="user", lazy = "dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


class contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    contact_skype_id = db.Column(db.String(128))
    contact_name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    groups = db.relationship("group", secondary= association_table, lazy = 'dynamic',
    back_populates = "contacts")



class group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group_name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contacts = db.relationship("contact", secondary= association_table, lazy = 'dynamic',
    back_populates = "groups")
    



class message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    skype_sender_name = db.Column(db.String(128))
    skype_message_id = db.Column(db.Integer)
    chat_id = db.Column(db.String(128))
    skype_account = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column (db.String())
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)
