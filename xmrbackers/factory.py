import quart.flask_patch
from quart import Quart
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from xmrbackers.cli import cli
from xmrbackers import config


async def _setup_db(app: Quart):
    import peewee
    import xmrbackers.models
    model = peewee.Model.__subclasses__()
    for m in model:
        m.create_table()

def create_app():
    app = Quart(__name__)
    app.config.from_envvar('QUART_SECRETS')
    app = cli(app)
    @app.before_serving
    async def startup():
        from xmrbackers.routes import meta, api, auth
        from xmrbackers import filters
        await _setup_db(app)
        app.register_blueprint(meta.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(filters.bp)
        login_manager = LoginManager(app)

        # Login manager
        login_manager.login_view = 'auth.login'
        login_manager.logout_view = 'auth.logout'

        @login_manager.user_loader
        def load_user(user_id):
            from xmrbackers.models import User
            user = User.get(user_id)
            return user
    return app

bcrypt = Bcrypt(create_app())
