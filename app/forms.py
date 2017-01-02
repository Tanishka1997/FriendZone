from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Length

class LoginForm(Form):
    UserName=StringField('username',validators=[DataRequired()])
    Password=PasswordField('password',validators=[DataRequired()])
    remember_me=BooleanField('remember_me',default=False)

class RegisterForm(Form):
    Username = StringField('username', validators=[Length(min=4, max=25),DataRequired()])
    Email = StringField('Email Address', validators=[Length(min=6, max=35),DataRequired()])
    Password = PasswordField('New Password',
        validators=[DataRequired(),EqualTo('confirm', message='Passwords must match'),DataRequired(),Length(min=6)])
    confirm = PasswordField('Repeat Password')

class EditForm(Form):
    Username=StringField('username',validators=[DataRequired()])
    AboutMe=TextAreaField('about_me',validators=[Length(min=0,max=140)])
