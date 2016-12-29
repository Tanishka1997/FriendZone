from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Length

class LoginForm(Form):
    UserName=StringField('username',validators=[DataRequired()])
    Password=PasswordField('password',validators=[DataRequired()])
    remember_me=BooleanField('remember_me',default=False)

class RegisterForm(Form):
    Username = StringField('username', validators=[Length(min=4, max=25)])
    Email = StringField('Email Address', validators=[Length(min=6, max=35)])
    Password = PasswordField('New Password',
        validators=[DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
