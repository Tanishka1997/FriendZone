from app import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.String(35),index=True,unique=True,nullable=False)
    email=db.Column(db.String(35),index=True,unique=True,nullable=False)
    password=db.Column(db.String(35),index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.user)


class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    time=db.Column(db.DateTime)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post %r>' % (self.body)
