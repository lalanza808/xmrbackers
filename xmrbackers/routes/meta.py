from quart import Blueprint, render_template
from flask_login import current_user

from xmrbackers.models import CreatorProfile, Subscription, TextPost


bp = Blueprint('meta', 'meta')

@bp.route('/')
async def index():
    feed = None
    if current_user.is_authenticated:
        backer = current_user.backer_profile.first()
        new_creators = CreatorProfile.select().where(
            CreatorProfile.verified == True
        ).order_by(CreatorProfile.create_date.desc()).execute()
        active_subscriptions = Subscription.select().where(
            Subscription.active == True,
            Subscription.backer == backer
        ).order_by(Subscription.subscribe_date.desc()).execute()
        new_posts = TextPost.select().where(
            TextPost.hidden == False,
            TextPost.creator in [c.creator for c in active_subscriptions]
        ).order_by(TextPost.post_date.desc()).execute()
        feed = {
            'new_creators': [i.user.username for i in new_creators],
            'new_posts': [i.title for i in new_posts],
            'active_subscriptions': [i.id for i in active_subscriptions]
        }
    return await render_template('index.html', feed=feed)
