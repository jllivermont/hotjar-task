import pytest

from peewee import *  # noqa
from playhouse.test_utils import test_database
from survey.models import SurveyResponse

test_db = SqliteDatabase(':memory:')


def test_create_user_with_all_fields_successful():
    with test_database(test_db, (SurveyResponse,)):
        SurveyResponse.create(
            name="James",
            email="j@j.com",
            age=35,
            about_me="developer",
            address="123 Big Street, Waunakee, WI, USA",
            gender="male",
            favorite_book="War & Peace",
            favorite_colors="red,blue,green")


def test_create_user_with_required_fields_successful():
    with test_database(test_db, (SurveyResponse,)):
        SurveyResponse.create(
            name="Nancy",
            email="nancy@gmail.com",
            age=62,
            about_me="I love gardening!!!")


def test_create_user_with_minimal_fields_successful():
    with test_database(test_db, (SurveyResponse,)):
        SurveyResponse.create(
            name="Pedro",
            email="p@asdfa.ie")


def test_user_with_existing_email_is_not_inserted():
    with test_database(test_db, (SurveyResponse,)):
        SurveyResponse.create(
            name="Nancy",
            email="nancy@gmail.com",
            age=62,
            about_me="I love gardening!!!")
        with pytest.raises(IntegrityError):
            SurveyResponse.create(
                name="Joan",
                email="nancy@gmail.com",
                age=63,
                about_me="I love gardening, too!!!")
