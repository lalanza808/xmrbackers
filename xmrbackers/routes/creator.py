from quart import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from monero.wallet import Wallet

from xmrbackers.forms import ConfirmSubscription
from xmrbackers.models import User, CreatorProfile, BackerProfile, TextPost
from xmrbackers.models import Subscription, SubscriptionMeta
from xmrbackers.helpers import check_tx_key
from xmrbackers import config


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
        form = ConfirmSubscription()
        return await render_template(
            'creator/subscription.html',
            subscription_meta=subscription_meta,
            form=form
        )
    else:
        await flash('That creator does not exist.')
        return redirect(url_for('meta.index'))

@bp.route('/subscription/<int:subscription_id>/confirm', methods=['POST'])
async def confirm_subscription(subscription_id):
    # do checks here for SubscriptionMeta assumption
    sm = SubscriptionMeta.get_or_none(subscription_id)
    form = ConfirmSubscription()
    if form.validate_on_submit():
        w = Wallet(
            port=8000,
            user=config.XMR_WALLET_RPC_USER,
            password=config.XMR_WALLET_RPC_PASS
        )
        check_data = {
            'txid': form.tx_id.data,
            'tx_key': form.tx_key.data,
            'address': form.wallet_address.data
        }
        try:
            res = w._backend.raw_request('check_tx_key', check_data)
        except:
            await flash(f'Invalid transaction! No subscription for you!')
            return redirect(url_for('creator.show', username=sm.creator.user.username))

        if res['received'] >= sm.atomic_xmr:
            backer_profile = BackerProfile.select().where(
                BackerProfile.user == current_user
            ).first()
            s = Subscription(
                creator=sm.creator.id,
                backer=backer_profile.id,
                meta=sm.id,
            )
            s.save()
            await flash(f'Found valid transaction! You are now subscribed to {sm.creator.user.username}!')
            return redirect(url_for('creator.show', username=sm.creator.user.username))
        else:
            await flash('Not enough XMR sent! No subscription for you!')
            return redirect(url_for('creator.show', username=sm.creator.user.username))
    else:
        await flash('Unable to accept form POST.')
        return redirect(url_for('meta.index'))
