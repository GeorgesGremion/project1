from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
import jwt
from app import app, db, login
from flask import url_for

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    food = db.Column(db.String(50), nullable=True)
    sleep_start = db.Column(db.DateTime, nullable=True)
    sleep_end = db.Column(db.DateTime, nullable=True)
    diaper_change_large = db.Column(db.DateTime, nullable=True)
    diaper_change_small = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    activity_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return '<Activity for child_id {} at {}>'.format(self.child_id, self.timestamp)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    group = db.Column(db.String(50)) 

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = {'extend_existing': True}


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    group = db.Column(db.String(50), nullable=False)
    activities = db.relationship('Activity', backref='child', lazy='dynamic')

    def __repr__(self):
        return '<Child {} {}>'.format(self.first_name, self.last_name)
    
    def delete(self):
        self.confirmation = True
        db.session.delete(self) 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
