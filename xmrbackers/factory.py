import quart.flask_patch
from quart import Quart

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
    @app.before_serving
    async def startup():
        from xmrbackers.routes import meta, api
        from xmrbackers import filters
        await _setup_db(app)
        app.register_blueprint(meta.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(filters.bp)

    return cli(app)
