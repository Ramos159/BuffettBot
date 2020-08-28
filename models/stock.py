from peewee import Model, CharField, SqliteDatabase


db = SqliteDatabase('database.db')


class Stock(Model):
    symbol = CharField()

    class Meta:
        database = db


db.create_tables([Stock])
