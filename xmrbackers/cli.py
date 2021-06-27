import click


def cli(app):
    @app.cli.command('echo')
    def echo():
        click.echo('Hello world!')

    return app
