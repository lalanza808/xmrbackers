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
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)

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
    id = pw.AutoField()
    user = pw.ForeignKeyField(User)
    create_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField(null=True)
    bio = pw.CharField()

    class Meta:
        database = db


class BackerProfile(pw.Model):
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


class SubscriptionMeta(pw.Model):
    id = pw.AutoField()
    create_date = pw.DateTimeField(default=datetime.now)
    creator = pw.ForeignKeyField(CreatorProfile)
    atomic_xmr = pw.BigIntegerField()
    number_hours = pw.IntegerField()

    def get_end_date(self) -> datetime:
        # some timedelta shiz
        pass

    class Meta:
        database = db


class Subscription(pw.Model):
    id = pw.AutoField()
    subscribe_date = pw.DateTimeField(default=datetime.now)
    active = pw.BooleanField(default=True)
    creator = pw.ForeignKeyField(CreatorProfile)
    backer = pw.ForeignKeyField(BackerProfile)
    meta = pw.ForeignKeyField(SubscriptionMeta)
    xmr_address = pw.CharField(unique=True)
    xmr_acct_idx = pw.BigIntegerField(unique=True) # in case it gets many subscribers
    xmr_addr_idx = pw.BigIntegerField(unique=True)

    class Meta:
        database = db

class TextPost(pw.Model):
    id = pw.AutoField()
    post_date = pw.DateTimeField(default=datetime.now)
    hidden = pw.BooleanField(default=False)
    content = pw.TextField()
    title = pw.CharField()
    last_edit_date = pw.DateTimeField(default=datetime.now)
    creator = pw.ForeignKeyField(CreatorProfile)

    class Meta:
        database = db
