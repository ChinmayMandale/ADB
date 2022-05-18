from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('GameRoom', validators=[DataRequired()])
    submit = SubmitField('Enter the Game LineG')
