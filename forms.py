from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators


class StatementForm(Form):
    statement = StringField('statement', validators=[validators.DataRequired(), validators.Regexp("""[^\";']""")])


class SignupForm(Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])


class LoginForm(Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me')
