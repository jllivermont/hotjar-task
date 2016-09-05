import os

from peewee import *  # noqa

TEST_DB_FILE = "local.db"

# Wipe the local test DB before each run
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

test_db = SqliteDatabase(TEST_DB_FILE)

prod_db = PostgresqlDatabase(
    os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
)

db = prod_db if "USE_PROD_DB" in os.environ else test_db
db_type = "prod" if "USE_PROD_DB" in os.environ else "test"


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


def db_init():
    db.connect()
    if db_type == "test":
        db.create_tables([SurveyResponse], True)


def db_close():
    if not db.is_closed():
        db.close()


db_init()
