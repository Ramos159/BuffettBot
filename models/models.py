from peewee import Model, IntegerField, CharField, SqliteDatabase


db = SqliteDatabase('database.db')


class GuildSetting(Model):
    discord_ID = IntegerField()
    prefix = CharField(default="?")
    news_channel_id = IntegerField(null=True)

    class Meta:
        database = db


db.create_tables([GuildSetting])
