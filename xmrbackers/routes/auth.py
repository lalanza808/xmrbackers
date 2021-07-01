import quart.flask_patch
from quart import Blueprint, render_template
from quart import flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from xmrbackers.factory import bcrypt
from xmrbackers.forms import Register, Login
from xmrbackers.models import User


bp = Blueprint('auth', 'auth')

@bp.route("/register", methods=["GET", "POST"])
async def register():
    form = Register()
    if current_user.is_authenticated:
        await flash('Already registered and authenticated.')
        return redirect(url_for('meta.index'))

    if form.validate_on_submit():
        # Check if email already exists
        user = User.select().where(
            User.email == form.email.data
        ).first()
        if user:
            await flash('This email is already registered.')
            return redirect(url_for('auth.login'))

        # Save new user
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf8'),
        )
        user.save()
        login_user(user)
        return redirect(url_for('meta.index'))

    return await render_template("auth/register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
async def login():
    form = Login()
    if current_user.is_authenticated:
        await flash('Already logged in.')
        return redirect(url_for('meta.index'))

    if form.validate_on_submit():
        # Check if user doesn't exist
        user = User.select().where(
            User.email == form.email.data
        ).first()
        if not user:
            await flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        # Check if password is correct
        password_matches = bcrypt.check_password_hash(
            user.password,
            form.password.data
        )
        if not password_matches:
            await flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('meta.index'))

    return await render_template("auth/login.html", form=form)

@bp.route("/logout")
async def logout():
    if current_user.is_authenticated:
        logout_user()
    else:
        await flash('Not authenticated!')
    return redirect(url_for('meta.index'))

# @auth_bp.route("/reset/<string:hash>", methods=["GET", "POST"])
# def reset(hash):
#     hash = PasswordReset.query.filter(PasswordReset.hash==hash).first()
#     if not hash:
#         flash('Invalid password reset hash')
#         return redirect(url_for('auth.login'))
#
#     if hash.hours_elapsed() > hash.expiration_hours or hash.expired:
#         flash('Reset hash has expired')
#         return redirect(url_for('auth.login'))
#
#     form = ResetPassword()
#     if form.validate_on_submit():
#         try:
#             user = User.query.get(hash.user)
#             user.password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
#             hash.expired = True
#             db.session.commit()
#             flash('Password reset successfully')
#             return redirect(url_for('auth.login'))
#         except:
#             flash('Error resetting password')
#             return redirect(url_for('auth.login'))
#
#     return render_template('auth/reset.html', form=form)
