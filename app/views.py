from app import app
from flask import render_template,flash,redirect
from .forms import LoginForm,RegisterForm
from app import db
from .models import User

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
		return redirect('/index')
	return (render_template('login.html',title='Sign In',form=form))

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		new_user=User(user=form.Username.data,email=form.Email.data,password=str(form.Password.data))
		db.session.add(new_user)
		try:
			db.session.commit()
			return redirect('/index')
		except Exception as e:
			return redirect('/login')

	return (render_template('register.html',title='Register',form=form))
