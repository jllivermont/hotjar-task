import re
import string


def normalize(data):
    """Normalizes the values of incoming data

    Args:
        data (dict): Dictionary of response data

    Returns:
        dict
    """

    normalized_data = {}

    for key in data:
        value = data[key]
        key = key.lower()

        # Strip all fields and reduce multiple spaces to a single whitespace
        value = value.strip()
        value = re.sub(r"\s+", " ", value)

        if key == "name":
            value = string.capwords(value)
        elif key == "age":
            value = int(value)
        elif key in ("gender", "favorite_colors"):
            value = value.lower()

        if key in ("email", "favorite_colors", "finished"):
            value = value.replace(" ", "")

        if key == "finished":
            value = bool(value.capitalize())

        normalized_data[key] = value

    return normalized_data
