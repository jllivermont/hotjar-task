from survey.error import ValidationError
from survey.models import SurveyResponse

from validate_email import validate_email

GENDERS = ("male", "female")
COLORS = (
    "red",
    "blue",
    "green",
    "brown",
    "black",
    "white",
    "orange",
    "pink",
    "yellow",
    "purple")


def _check_max_length(field_name, value):
    """Check whether the length of a field value exceeds the max size"""

    # Figure out the max length from the DB schema
    column = getattr(SurveyResponse, field_name)
    max_length = getattr(column, "max_length", None)

    if max_length is not None:
        error_msg = "Value for field {0} exceeds max length of {1} characters"

        if len(value) > max_length:
            raise ValidationError(error_msg.format(field_name, max_length))


def _check_in_range(field_name, value, lower, upper):
    """Check that an integer value is within the specified range"""

    error_msg = "Value for field {0} is outside the range {1}-{2}"

    if (value < lower) or (value > upper):
        raise ValidationError(error_msg.format(field_name, lower, upper))


def _check_in_enum(field_name, value, enum):
    """Checks whether an enum-style value is represented in the enum"""

    error_msg = "Value for field {0} can only be one of these: {1}"

    if value not in enum:
        raise ValidationError(error_msg.format(field_name, str(enum)))


def _validate_name(name):
    _check_max_length("name", name)


def _validate_email(email):
    _check_max_length("email", email)

    if not validate_email(email):
        error_msg = "Value for field email is not a valid email address"
        raise ValidationError(error_msg)


def _validate_age(age):
    _check_in_range("age", age, 3, 125)


def _validate_about_me(about_me):
    _check_max_length("about_me", about_me)


def _validate_address(address):
    _check_max_length("address", address)


def _validate_gender(gender):
    _check_in_enum("gender", gender, GENDERS)


def _validate_favorite_book(favorite_book):
    _check_max_length("favorite_book", favorite_book)


def _validate_favorite_colors(favorite_colors):
    if "," in favorite_colors:
        favorite_colors = favorite_colors.split(",")

    if isinstance(favorite_colors, list) or isinstance(favorite_colors, tuple):
        for color in favorite_colors:
            _check_in_enum("favorite_colors", color, COLORS)
    else:
        _check_in_enum("favorite_colors", favorite_colors, COLORS)


def _validate_field(field_name, field_value):
    """Validates the normalized value for the specified field"""

    func_name = "_validate_{}".format(field_name)
    if func_name not in globals():
        raise ValueError(
            "Unknown field {0} can't be validated".format(field_name))

    # Invoke the validation function
    globals()[func_name](field_value)


def _validate_mandatory_fields(data, required_fields):
    """Ensure that all of the mandatory fields are in the input data"""
    for field in required_fields:
        if field not in data:
            raise ValidationError("Missing mandatory field {}".format(field))


def _validate_forbidden_fields(data, forbidden_fields):
    """Ensure that that any forbidden fields are NOT in the input data"""
    for field in forbidden_fields:
        if field in data:
            raise ValidationError(
                "Field {} is not allowed for this operation".format(field))


def validate(data, required_fields=None, forbidden_fields=None):
    """Validates each key-value pair

    Args:
        data (dict): Incoming data from request
        required_fields (list): Mandatory fields
        forbidden_fields (list): Forbidden fields
    """

    if required_fields is not None:
        _validate_mandatory_fields(data, required_fields)

    if forbidden_fields is not None:
        _validate_forbidden_fields(data, forbidden_fields)

    for key, value in data.items():
        _validate_field(key, value)
