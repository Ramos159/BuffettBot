from peewee import Model, IntegerField, CharField, SqliteDatabase, ForeignKeyField
from models import Guild

db = SqliteDatabase('database.db')


class GuildSetting(Model):
    guild = ForeignKeyField(Guild)
    prefix = CharField(default="?")
    news_channel_id = IntegerField(null=True)

    class Meta:
        database = db


db.create_tables([GuildSetting])
