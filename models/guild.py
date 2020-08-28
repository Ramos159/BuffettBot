from peewee import Model, IntegerField, CharField, SqliteDatabase


db = SqliteDatabase('database.db')


class Guild(Model):
    discord_id = IntegerField()

    class Meta:
        database = db


db.create_tables([Guild])
