import flask_wtf
import wtforms


class IntegerRangeField(wtforms.IntegerField):
    widget = wtforms.widgets.Input(input_type="range")


class DifficultyForm(flask_wtf.FlaskForm):
    difficulty = IntegerRangeField('difficulty')


class TrueOrFalseForm(flask_wtf.FlaskForm):
    choice = wtforms.RadioField(choices=[('True', 'TRUE'), ('False', 'FALSE')],
                                validators=[wtforms.validators.InputRequired()])
    hidden = wtforms.HiddenField()


class StatementForm(flask_wtf.FlaskForm):
    statement = wtforms.StringField('statement', validators=[wtforms.validators.InputRequired(),
                                                             wtforms.validators.Regexp("""[^\";']""")])


class SignupForm(flask_wtf.FlaskForm):
    email = wtforms.StringField('email', validators=[wtforms.validators.InputRequired(), wtforms.validators.Email()])
    username = wtforms.StringField('username', validators=[wtforms.validators.InputRequired()])
    password = wtforms.PasswordField('password', validators=[wtforms.validators.InputRequired(),
                                                             wtforms.validators.EqualTo('verify',
                                                                                        message='Passwords must match.')])
    verify = wtforms.PasswordField('verify', validators=[wtforms.validators.InputRequired()])
    register = wtforms.SubmitField('Register')


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('username', validators=[wtforms.validators.InputRequired()])
    password = wtforms.PasswordField('password', validators=[wtforms.validators.InputRequired()])
    remember_me = wtforms.BooleanField('remember_me')
    login = wtforms.SubmitField('Log in')
