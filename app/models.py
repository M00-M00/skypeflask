from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from flask import current_app
from flask_table import Table, Col
from time import time
import jwt

followed_securities = db.Table('followed_securities',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("security_id", db.Integer, db.ForeignKey("security.id")))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index = True, unique = True)
    transactions = db.relationship('Transaction', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    securities = db.relationship("Security", secondary= followed_securities, lazy = 'dynamic',
    backref = db.backref("users", lazy = True))

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

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def follow_or_unfollow(self,security):
        if not self.is_following(security):
            self.securities.append(security)
            flash("Ticker Is Followed")
        else:
            self.securities.remove(security)
            flash("Ticker Is Unfollowed")

    def follow(self, security):
        if not self.is_following(security):
            self.securities.append(security)

    def unfollow(self, security):
        if self.is_following(security):
            self.securities.remove(security)

    def is_following(self, security):
        return self.securities.filter(
        followed_securities.c.security_id == security.id).count()>0

    def followed_tickers(self):
        tickers_list = []
        for s in self.securities.all():
            tickers_list.append(s.ticker)
        return tickers_list


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'))
    long = db.Column(db.Boolean, default= False,  nullable=True)
    unit_price = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        l = "Long"
        s = "Short"
        x = str()
        if self.long == True :
            x = l
        else:
            x = s
        return  '<{} {} for {} >'.format(x, self.subscriber, self.total_cost)

class Security(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(64), index = True)
    tx_security = db.relationship("Transaction", backref='subscriber', lazy='dynamic')
    sector = db.Column(db.String(64), index = True)
    name = db.Column(db.String(128), index = True)
    website = db.Column(db.String(64), index = True)
    summary = db.Column(db.String(), index = True)



    def __repr__(self):
        return '<Ticker {}>'.format(self.ticker)


class ItemTable(Table):
     ticker = Col("Ticker")
     sector = Col('Sector')
     name = Col('Name')
     website = Col('Website')
     summary = Col('Summary')
