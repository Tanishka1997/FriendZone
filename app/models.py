from app import db
from flask.ext.login import UserMixin
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    social_id=db.Column(db.String(64),unique=True)
    user=db.Column(db.String(35),index=True,unique=True,nullable=False)
    email=db.Column(db.String(35),index=True,unique=True,nullable=False)
    password=db.Column(db.String(35))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)


    def __repr__(self):
        return '<User %r>' % (self.user)


class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    time=db.Column(db.DateTime)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post %r>' % (self.body)
