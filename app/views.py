from app import app
from flask import render_template,flash,redirect,url_for
from .forms import LoginForm,RegisterForm
from app import db
from .models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_,and_
@app.route('/')
@app.route('/index')
def index():
	user={'nickname':'Tanishka'}
	posts=[]
	return (render_template('index.html',title='Home',user=user,posts=posts))

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		if User.query.filter(and_(User.user==form.UserName.data,User.password==form.Password.data)).count()>0:
			return redirect('/index')
		else:
			flash("Invalid Username or Password")
			return redirect(url_for('login'))
	return (render_template('login.html',title='Sign In',form=form))

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
	if form.validate_on_submit():

		if User.query.filter(or_(User.user==form.Username.data,User.email==form.Email.data)).count()>0:
			flash("Username and email for any User must be unique.Try registering again")
			return redirect('/register')
		else:
			new_user=User(user=form.Username.data,email=form.Email.data,password=str(form.Password.data))
			db.session.add(new_user)
			db.session.commit()
			flash("Successfully registered with FriendZone")
			return redirect('/index')

	return (render_template('register.html',title='Register',form=form))
