import flask_wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, HiddenField
from wtforms import validators


class TrueOrFalseForm(flask_wtf.FlaskForm):
    choice = RadioField(choices=[('True', 'TRUE'), ('False', 'FALSE')], validators=[validators.InputRequired()])
    hidden = HiddenField()


class StatementForm(flask_wtf.FlaskForm):
    statement = StringField('statement', validators=[validators.InputRequired(), validators.Regexp("""[^\";']""")])


class SignupForm(flask_wtf.FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email()])
    username = StringField('username', validators=[validators.InputRequired()])
    password = PasswordField('password', validators=[validators.InputRequired(),
                                                     validators.EqualTo('verify', message='Passwords must match.')])
    verify = PasswordField('verify', validators=[validators.InputRequired()])
    register = SubmitField('Register')


class LoginForm(flask_wtf.FlaskForm):
    username = StringField('username', validators=[validators.InputRequired()])
    password = PasswordField('password', validators=[validators.InputRequired()])
    remember_me = BooleanField('remember_me')
    login = SubmitField('Log in')
