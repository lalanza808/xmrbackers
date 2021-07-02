# import quart.flask_patch
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UserAuth(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "form-control", "type": "text"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})
