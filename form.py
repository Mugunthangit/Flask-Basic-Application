from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditForm(Form):
    password = StringField('password', validators=[DataRequired()])
    Retype_password = StringField('Retype_password', validators=[Length(min=0, max=140)])

class Update(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])

class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    Retype_password = StringField('Retype_password', validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
