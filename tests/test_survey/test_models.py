import pytest

from peewee import IntegrityError
from survey.models import SurveyResponse


def test_create_user_with_all_fields_successful():
    return SurveyResponse.create(
        name="James",
        email="j@j.com",
        age=35,
        about_me="developer",
        address="123 Big Street, Waunakee, WI, USA",
        gender="male",
        favorite_book="War & Peace",
        favorite_colors="red,blue,green")


def test_create_user_with_minimum_required_fields_successful():
    SurveyResponse.create(
        name="Nancy",
        email="nancy@gmail.com",
        age=62,
        about_me="I love gardening!!!")


def test_create_user_with_minimum_model_fields_successful():
    SurveyResponse.create(
        name="Pedro",
        email="p@asdfa.ie")


def test_user_with_existing_email_is_not_inserted():
    SurveyResponse.create(
        name="Rosa",
        email="rosasita@yahoo.com",
        age=62,
        about_me="I love birds")
    with pytest.raises(IntegrityError):
        SurveyResponse.create(
            name="Joan",
            email="rosasita@yahoo.com",
            age=63,
            about_me="I love gardening, too!!!")
