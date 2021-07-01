from datetime import datetime

import peewee as pw

from xmrbackers import config


db = pw.PostgresqlDatabase(
    config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
)


class Creator(pw.Model):
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
    bio = pw.CharField()

    class Meta:
        database = db


class Backer(pw.Model):
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)

    class Meta:
        database = db


class SubscriptionMeta(pw.Model):
    id = pw.AutoField()
    create_date = pw.DateTimeField(default=datetime.now)
    creator = pw.ForeignKeyField(Creator)
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
    creator = pw.ForeignKeyField(Creator)
    backer = pw.ForeignKeyField(Backer)
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
    creator = pw.ForeignKeyField(Creator)

    class Meta:
        database = db
