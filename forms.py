import flask_wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators


class StatementForm(flask_wtf.Form):
    statement = StringField('statement', validators=[validators.DataRequired(), validators.Regexp("""[^\";']""")])


class SignupForm(flask_wtf.Form):
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.EqualTo('verify', message='Passwords must match.')])
    verify = PasswordField('verify', validators=[validators.DataRequired()])
    register = SubmitField('Register')


class LoginForm(flask_wtf.Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me')
    login = SubmitField('Log in')
