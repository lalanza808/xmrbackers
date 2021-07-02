from datetime import datetime

import peewee as pw

from xmrbackers import config


db = pw.PostgresqlDatabase(
    config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
)

class User(pw.Model):
    """
    User model is for pure user authentication management
    and reporting.
    """
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    username = pw.CharField(unique=True)
    password = pw.CharField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id

    class Meta:
        database = db

class CreatorProfile(pw.Model):
    """
    CreatorProfile model is for creators to provide metadata about
    themselves for their fans or even just the general public.
    Links to social media, contact info, portfolio sites, etc
    should go in here.
    """
    id = pw.AutoField()
    user = pw.ForeignKeyField(User)
    create_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField(null=True)
    website = pw.CharField(null=True)
    twitter_handle = pw.CharField(null=True)
    email = pw.CharField(unique=True, null=True)
    bio = pw.CharField()
    verified = pw.CharField(default=False)

    class Meta:
        database = db


class BackerProfile(pw.Model):
    """
    BackerProfile model is for backers to give contact info
    if they wanted to retain communications in some way...ie
    recurring emails and/or notifications. For now.
    """
    id = pw.AutoField()
    user = pw.ForeignKeyField(User, backref='backer_profile')
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    email = pw.CharField(unique=True, null=True)

    class Meta:
        database = db


class SubscriptionMeta(pw.Model):
    """
    SubscriptionMeta model is for the Creator to define details about
    their subscription plan to release for subscribers. There is no
    editing in place, only creating new plans; anyone utilizing an
    existing subscription (by loading it on screen) will be grandfathered in.
    """
    id = pw.AutoField()
    create_date = pw.DateTimeField(default=datetime.now)
    creator = pw.ForeignKeyField(CreatorProfile)
    atomic_xmr = pw.BigIntegerField()
    number_hours = pw.IntegerField()
    wallet_address = pw.CharField()

    def get_end_date(self) -> datetime:
        # some timedelta shiz
        pass

    class Meta:
        database = db


class Subscription(pw.Model):
    """
    Subscription model gets created when backers can confirm payment via
    the `check_tx_key` RPC method. Once a subscription is in place and is
    associated with a user, that user is then elligible to view that
    creator's content.
    """
    id = pw.AutoField()
    subscribe_date = pw.DateTimeField(default=datetime.now)
    active = pw.BooleanField(default=True)
    creator = pw.ForeignKeyField(CreatorProfile)
    backer = pw.ForeignKeyField(BackerProfile)
    meta = pw.ForeignKeyField(SubscriptionMeta)

    class Meta:
        database = db

class TextPost(pw.Model):
    """
    TextPost model is the first content type available to post. Metadata
    here is basic for now, let's proof out the other components first.
    """
    id = pw.AutoField()
    post_date = pw.DateTimeField(default=datetime.now)
    hidden = pw.BooleanField(default=False)
    content = pw.TextField()
    title = pw.CharField()
    last_edit_date = pw.DateTimeField(default=datetime.now)
    creator = pw.ForeignKeyField(CreatorProfile)

    class Meta:
        database = db
