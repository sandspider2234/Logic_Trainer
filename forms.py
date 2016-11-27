import flask_wtf
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators


class StatementForm(flask_wtf.Form):
    statement = StringField('statement', validators=[validators.DataRequired(), validators.Regexp("""[^\";']""")])


class SignupForm(flask_wtf.Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])


class LoginForm(flask_wtf.Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me')
