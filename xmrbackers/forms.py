# import quart.flask_patch
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UserAuth(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "form-control", "type": "text"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})

class ConfirmSubscription(FlaskForm):
    tx_id = StringField('TX ID:', validators=[DataRequired()], render_kw={"placeholder": "TX ID", "class": "form-control", "type": "text"})
    tx_key = StringField('TX Key:', validators=[DataRequired()], render_kw={"placeholder": "TX Key", "class": "form-control", "type": "text"})
    wallet_address = StringField('XMR Address:', validators=[DataRequired()], render_kw={"placeholder": "XMR Address", "class": "form-control", "type": "text"})
