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
    last_read_time = db.Column(db.DateTime)


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

    def new_messages(self):
        last_read_time = self.last_read_time or datetime(1900, 1, 1)
        return message.query.filter_by(user_id = self.id).filter(
            message.timestamp > last_read_time).count()


class contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    contact_skype_id = db.Column(db.String(128))
    contact_name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    groups = db.relationship("group", secondary= association_table, lazy = 'dynamic',
    back_populates = "contacts")

    def unread_count(self):
        msgs = message.query.filter_by(chat_id = f"8:{self.contact_skype_id}", read = False).all()
        if msgs != None:
            count = 0
        else:
            count = len(msgs)
        print(count)
        return count


    @staticmethod
    def _unread_count(contact_skype_id):
        msgs = message.query.filter_by(chat_id = "8:" + contact_skype_id, read = False).all()
        if msgs == None:
            count = 0
        else:
            count = len(msgs)
        return count
        
    @staticmethod
    def all_unread_count():
        msgs = message.query.filter_by(read = False).all()
        ids = [m.skype_sender_name for m in msgs if m.skype_sender_name != current_app.config["SKYPE_USERID"]]
        ids = list(set(ids))
        
        return ids



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
    read = db.Column (db.Boolean, default = False)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)

    def mark_read(self):
        self.read = True
        db.session.commit()


    @staticmethod
    def contains_unread(skype_account):
        msgs = self.query.filter_by(skype_sender_name = skype_account, read = False).first()
        if msgs != None:
            return True
        else:
            return False
    
    @staticmethod
    def mark_as_read(skype_acc):
        #msgs = message.query.filter_by(skype_sender_name = skype_account, read = False).all()
        #msgs.update(read = True)
        db.session.query(message).filter_by(skype_sender_name = skype_acc).update({'read': True})
        db.session.commit()
