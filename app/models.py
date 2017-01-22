from app import db
from hashlib import md5
from flask_login import UserMixin

followers=db.Table('followers',db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),db.Column('followed_id',db.Integer,db.ForeignKey('user.id')))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    social_id=db.Column(db.String(64),unique=True)
    user=db.Column(db.String(35),index=True,unique=True,nullable=False)
    email=db.Column(db.String(35),index=True,unique=True,nullable=False)
    password=db.Column(db.String(35))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me=db.Column(db.String(140))
    last_seen=db.Column(db.DateTime)
    followed=db.relationship('User',secondary='followers',primaryjoin=(followers.c.follower_id==id),secondaryjoin=(followers.c.followed_id==id),backref=db.backref('followers',lazy='dynamic'),lazy='dynamic')

    def avatar(self,size):
        return ('http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(self.email.encode('utf-8')).hexdigest(),size))

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

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def __repr__(self):
        return '<User %r>' % (self.user)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    time=db.Column(db.DateTime)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post %r>' % (self.body)
