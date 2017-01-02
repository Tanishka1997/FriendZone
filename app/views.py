from app import app
from flask import render_template,flash,redirect,url_for,request,g,session
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm,RegisterForm,EditForm
from app import db,lm
from .models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_,and_
from .oauth import OAuthSignIn
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
	user=g.user
	posts=[]

	return (render_template('index.html',title='Home',user=user,posts=posts))

@app.route('/user/<user>')
@login_required
def user(user):
	user=User.query.filter_by(user=user).first()
	posts=[]
	if user is None:
		flash('User %s not found' %user)
		return (redirect(url_for('index')))
	return (render_template('user.html',user=user,posts=posts))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen=datetime.utcnow()
		db.session.query(User).filter_by(user=g.user.user).update({User.last_seen:g.user.last_seen})
		db.session.commit()

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		if User.query.filter(and_(User.user==form.UserName.data,User.password==form.Password.data)).count()>0:
			session['remember_me']=form.remember_me.data
			if 'remember_me' in session:
				remember_me=session['remember_me']
				session.pop('remember_me',None)
			user = User.query.filter(User.user==form.UserName.data).first()
			login_user(user,remember=remember_me)
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash("Invalid Username or Password")
			return redirect(url_for('login'))
	return (render_template('login.html',title='Sign In',form=form))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form=EditForm()
	if form.validate_on_submit():
		if User.query.filter(User.user==form.Username.data).count()==0:
			g.user.user=form.Username.data
			g.user.about_me=form.AboutMe.data
			db.session.query(User).filter_by(user=g.user.user).update({User.user:form.Username.data})
			db.session.query(User).filter_by(user=g.user.user).update({User.about_me:form.AboutMe.data})
			db.session.commit()
			flash("Your have edited your profile Successfully")
			return redirect(url_for('edit'))
		else:
			flash("Username is already used by another user")
	else:
		form.Username.data=g.user.user
		form.AboutMe.data=g.user.about_me
	return render_template('edit.html',form=form)

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
			login_user(new_user,True)
			return redirect(request.args.get('next') or url_for('index'))
	return (render_template('register.html',title='Register',form=form))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth=OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth=OAuthSignIn.get_provider(provider)
	social_id,user_name,email=oauth.callback()
	if social_id is None:
		flash("Authentication Failed")
		return (redirect(url_for('login')))
	user=User.query.filter_by(social_id=social_id).first()
	if not user:
		user = User(social_id=social_id, user=user_name, email=email)
		db.session.add(user)
		db.session.commit()
	login_user(user, True)
	return redirect(url_for('index'))
