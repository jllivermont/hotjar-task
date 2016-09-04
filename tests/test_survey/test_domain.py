import pytest

from survey import domain


def test_create_response():
    input_dict = {"name": "james", "email": "jj@asdfasd.com"}
    id = domain.create_response(input_dict)
    response_dict = domain.get_response(id)
    assert response_dict["name"] == "james"
    assert response_dict["email"] == "jj@asdfasd.com"


def test_update_response():
    input_dict = {"name": "bill gates", "email": "bill@msft.com"}
    id = domain.create_response(input_dict)

    update_dict = {"age": 62, "address": "1 Gates Lane", "gender": "male"}
    domain.update_response(id, update_dict)

    update_dict = {
        "favorite_book": "Basic Programming",
        "favorite_colors": "red"}
    domain.update_response(id, update_dict)

    response_dict = domain.get_response(id)
    assert response_dict["age"] == 62
    assert response_dict["address"] == "1 Gates Lane"
    assert response_dict["gender"] == "male"
    assert response_dict["favorite_book"] == "Basic Programming"
    assert response_dict["favorite_colors"] == "red"


def test_multiple_updates():
    input_dict = {"name": "Tina Turner", "email": "tina@the80s.org"}
    id = domain.create_response(input_dict)

    update_dict = {"age": 32}
    domain.update_response(id, update_dict)

    update_dict = {"age": 45}
    domain.update_response(id, update_dict)

    response_dict = domain.get_response(id)
    assert response_dict["age"] == 45


def test_update_ignores_extra_keys():
    input_dict = {"name": "Julius Caesar", "email": "jc@rome.gov"}
    id = domain.create_response(input_dict)

    update_dict = {"address": "The Palace, 1 Appian Way, Rome", "foo": "bar"}
    domain.update_response(id, update_dict)

    response_dict = domain.get_response(id)
    assert "foo" not in response_dict


def test_finish_on_incomplete_response_raises_error():
    input_dict = {"name": "bob", "email": "bob@asdfa.org"}
    id = domain.create_response(input_dict)
    with pytest.raises(AssertionError):
        domain.finish(id)


def test_response_finishes():
    input_dict = {
        "name": "tim o'shea",
        "email": "blah@foobar.ie",
        "age": 32,
        "about_me": "nothing"}
    id = domain.create_response(input_dict)
    domain.update_response(id, input_dict)
    response_dict = domain.get_response(id)
    assert response_dict["finished"] is False

    domain.finish(id)
    response_dict = domain.get_response(id)
    assert response_dict["finished"] is True
