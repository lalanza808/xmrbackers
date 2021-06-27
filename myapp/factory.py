import quart.flask_patch
from quart import Quart
from flask_sqlalchemy import SQLAlchemy

from myapp import config


db = SQLAlchemy()

async def _setup_db(app: Quart):
    uri = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        user=config.DB_USER,
        pw=config.DB_PASS,
        host=config.DB_HOST,
        port=config.DB_PORT,
        db=config.DB_NAME
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

def create_app():
    app = Quart(__name__)
    app.config.from_envvar('QUART_SECRETS')


    @app.before_serving
    async def startup():
        from myapp.routes import meta, api
        from myapp import filters
        await _setup_db(app)
        app.register_blueprint(meta.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(filters.bp)
        # app.register_blueprint(cli.bp)

    return app
