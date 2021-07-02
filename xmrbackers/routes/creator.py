from quart import Blueprint, render_template, flash, redirect, url_for

from xmrbackers.models import User, CreatorProfile, TextPost, SubscriptionMeta


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
        posts = TextPost.select().where(
            TextPost.creator == creator,
            TextPost.hidden == False
        ).order_by(TextPost.post_date.desc())
        return await render_template(
            'creator/creator.html',
            creator=creator,
            posts=posts
        )
    else:
        await flash('That creator does not exist.')
        return redirect(url_for('meta.index'))

@bp.route('/creator/<username>/subscription')
async def subscription(username):
    user = User.select().where(User.username == username)
    creator = CreatorProfile.select().where(
        CreatorProfile.user == user
    )
    if creator:
        subscription_meta = SubscriptionMeta.select().where(
            SubscriptionMeta.creator == creator
        ).order_by(SubscriptionMeta.create_date.desc()).first()
        return await render_template(
            'creator/subscription.html',
            subscription_meta=subscription_meta
        )
    else:
        await flash('That creator does not exist.')
        return redirect(url_for('meta.index'))
