import click
from quart import Blueprint, current_app

from myapp.models import MyThing
from myapp.factory import db


bp = Blueprint('filters', 'filters')

@bp.cli.command('init')
def init():
    import app.models
    db.create_all()

@bp.cli.command('delete')
@click.argument('thing_id')
def delete(thing_id):
    thing = MyThing.query.get(thing_id)
    if thing:
        db.session.delete(thing)
        db.session.commit()
        click.echo(f'MyThing {thing.id} was deleted')
    else:
        click.echo('MyThing ID does not exist')

@bp.cli.command('list')
def list_things():
    thing = MyThing.query.all()
    for i in thing:
        click.echo(i.id)
