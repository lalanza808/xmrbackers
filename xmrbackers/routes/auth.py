import quart.flask_patch
from quart import Blueprint, render_template
from quart import flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from xmrbackers.factory import bcrypt
from xmrbackers.forms import Register
from xmrbackers.models import User


bp = Blueprint('auth', 'auth')

@bp.route("/register", methods=["GET", "POST"])
async def register():
    form = Register()
    # if current_user.is_authenticated:
        # flash('Already registered and authenticated.')
        # return redirect(url_for('meta.index'))
        # return 'gotem'
    if form.validate_on_submit():
        # Check if email already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('This email is already registered.')
            # return redirect(url_for('auth.login'))
            return 'gotem'

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
#
# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     form = Login()
#     if current_user.is_authenticated:
#         flash('Already registered and authenticated.')
#         return redirect(url_for('wallet.dashboard'))
#
#     if form.validate_on_submit():
#         # Check if user doesn't exist
#         user = User.query.filter_by(email=form.email.data).first()
#         if not user:
#             flash('Invalid username or password.')
#             return redirect(url_for('auth.login'))
#
#         # Check if password is correct
#         password_matches = bcrypt.check_password_hash(
#             user.password,
#             form.password.data
#         )
#         if not password_matches:
#             flash('Invalid username or password.')
#             return redirect(url_for('auth.login'))
#
#         # Capture event, login user, and redirect to wallet page
#         capture_event(user.id, 'login')
#         login_user(user)
#         return redirect(url_for('wallet.dashboard'))
#
#     return render_template("auth/login.html", form=form)
#
# @auth_bp.route("/logout")
# def logout():
#     if current_user.is_authenticated:
#         docker.stop_container(current_user.wallet_container)
#         capture_event(current_user.id, 'stop_container')
#         current_user.clear_wallet_data()
#         capture_event(current_user.id, 'logout')
#         logout_user()
#     return redirect(url_for('meta.index'))
#
# @auth_bp.route("/delete", methods=["GET", "POST"])
# @login_required
# def delete():
#     form = Delete()
#     if form.validate_on_submit():
#         docker.stop_container(current_user.wallet_container)
#         capture_event(current_user.id, 'stop_container')
#         sleep(1)
#         docker.delete_wallet_data(current_user.id)
#         capture_event(current_user.id, 'delete_wallet')
#         current_user.clear_wallet_data(reset_password=True, reset_wallet=True)
#         flash('Successfully deleted wallet data')
#         return redirect(url_for('wallet.setup'))
#     else:
#         flash('Please confirm deletion of the account')
#         return redirect(url_for('wallet.dashboard'))
#
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
