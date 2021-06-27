import click


def cli(app):
    @app.cli.command('init')
    def init():
        import xmrbackers.models
        from xmrbackers.factory import db
        db.create_all()

    return app
