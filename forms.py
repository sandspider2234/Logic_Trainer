from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class StatementForm(Form):
    statement = StringField('statement', validators=[DataRequired()])
