import click
from quart import Blueprint, current_app

from xmrbackers.models import Creator
from xmrbackers.factory import db


bp = Blueprint('cli', 'cli')

@bp.cli.command('init')
def init():
    import app.models
    db.create_all()

@bp.cli.command('delete')
@click.argument('thing_id')
def delete(thing_id):
    thing = Creator.query.get(thing_id)
    if thing:
        db.session.delete(thing)
        db.session.commit()
        click.echo(f'Creator {thing.id} was deleted')
    else:
        click.echo('Creator ID does not exist')

@bp.cli.command('list')
def list_things():
    thing = Creator.query.all()
    for i in thing:
        click.echo(i.id)
