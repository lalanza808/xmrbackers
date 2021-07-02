from quart import Blueprint, render_template, flash, redirect

from xmrbackers.models import User, CreatorProfile


bp = Blueprint('creator', 'creator')

@bp.route('/creators')
async def all():
    creators = CreatorProfile.select().order_by(
        CreatorProfile.create_date.desc()
    )
    return await render_template('creator/creators.html', creators=creators)

@bp.route('/creator/<username>')
async def show(username):
    user = User.select().where(User.username == username)
    creator = CreatorProfile.select().where(
        CreatorProfile.user == user
    ).first()
    if creator:
        return await render_template('creator/creator.html', creator=creator)
    else:
        flash('That creator does not exist.')
        return redirect(url_for('meta.index'))
