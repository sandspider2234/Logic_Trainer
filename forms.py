from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class StatementForm(Form):
    statement = StringField('statement', validators=[validators.DataRequired(), validators.Regexp("""[^\";']""")])
