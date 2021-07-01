import quart.flask_patch
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "form-control", "type": "text"})
    email = StringField('Email Address:', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "form-control", "type": "email"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})

class Register(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "form-control", "type": "text"})
    email = StringField('Email Address:', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "form-control", "type": "email"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})
