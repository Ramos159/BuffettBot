from peewee import Model, SqliteDatabase, ForeignKeyField
from models import Stock, Guild

db = SqliteDatabase('database.db')


class GuildStock(Model):
    guild = ForeignKeyField(Guild)
    stock = ForeignKeyField(Stock)

    class Meta:
        database = db


db.create_tables([GuildStock])
