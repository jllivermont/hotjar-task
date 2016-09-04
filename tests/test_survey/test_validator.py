import pytest

from survey.error import ValidationError
from survey.validator import validate_field


@pytest.mark.parametrize("field,value,error_expected", [
    ("age", 2, True),
    ("age", 3, False),
    ("age", 125, False),
    ("age", 126, True),
    ("name", 'x' * 93, True),
    ("name", 'x' * 92, False),
    ("gender", "male", False),
    ("gender", "female", False),
    ("gender", "boy", True),
    ("favorite_colors", "blue", False),
    ("favorite_colors", ("blue", "green"), False),
    ("favorite_colors", ("blue", "bird"), True),

])
def test_validate_field(field, value, error_expected):
    if error_expected:
        with pytest.raises(ValidationError):
            validate_field(field, value)
    else:
        validate_field(field, value)


@pytest.mark.parametrize("email,error_expected", [
    ("james@ibm.com", False),
    ("2323.com", True),
    ("****@**,**.ie", True),
    ("james@ib m.com", True),
])
def test_validate_email(email, error_expected):
    if error_expected:
        with pytest.raises(ValidationError):
            validate_field("email", email)
    else:
        validate_field("email", email)
