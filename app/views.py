from app import app
from flask import render_template,flash,redirect
from .forms import LoginForm,RegisterForm
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
