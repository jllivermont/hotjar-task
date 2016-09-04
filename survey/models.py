import os

from peewee import *  # noqa


test_db = SqliteDatabase(':memory:')

prod_db = PostgresqlDatabase(
    os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
)

db = prod_db if "USE_PROD_DB" in os.environ else test_db


class SurveyResponse(Model):
    name = CharField(max_length=92, null=False)
    email = CharField(max_length=128, null=False, unique=True, index=True)
    age = IntegerField(null=True)
    about_me = CharField(max_length=2048, null=True)
    address = CharField(max_length=1024, null=True)
    gender = CharField(max_length=6, null=True)
    favorite_book = CharField(max_length=256, null=True)
    favorite_colors = CharField(max_length=64, null=True)

    finished = BooleanField(default=False)

    class Meta:
        database = db

# Create the table if it doesn't exist
db.create_tables([SurveyResponse], safe=True)
