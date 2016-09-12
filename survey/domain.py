from survey.models import SurveyResponse


def _convert_response_to_dict(response):
    """Returns dictionary representation of SurveyResponse instance"""

    response_dict = {}
    response_dict["id"] = response.id
    response_dict["name"] = response.name
    response_dict["email"] = response.email
    response_dict["age"] = response.age
    response_dict["about_me"] = response.about_me
    response_dict["address"] = response.address
    response_dict["gender"] = response.gender
    response_dict["favorite_book"] = response.favorite_book
    response_dict["favorite_colors"] = response.favorite_colors
    response_dict["finished"] = response.finished

    return response_dict


def get_response(id):
    """Fetches the SurveyResponse for the specified ID

    Args:
        id (int): Primary key of the SurveyResponse to be returned

    Returns:
        dict
    """

    resp = SurveyResponse.get(SurveyResponse.id == id)
    return _convert_response_to_dict(resp)


def get_all_responses():
    """Fetches all SurveyResponses

    Returns:
        dict
    """

    responses = []

    for resp in SurveyResponse.select():
        responses.append(_convert_response_to_dict(resp))

    return responses


def create_response(data):
    """Creates a new SurveyResponse

    Args:
        data (dict): Values to be inserted into new SurveyResponse instance

    Returns:
        int: Primary key (id) of the newly inserted SurveyResponse
    """

    name = data["name"]
    email = data["email"]

    resp = SurveyResponse.create(name=name, email=email)
    return resp.id


def update_response(id, data):
    """Updates an existing SurveyResponse

    Args:
        id (int): Primary key of the SurveyResponse to be returned
        data (dict): Values to be inserted into new SurveyResponse instance
    """

    resp = SurveyResponse.get(SurveyResponse.id == id)

    for field in SurveyResponse._meta.sorted_field_names:
        if field in data and field != "finished":
            setattr(resp, field, data[field])

    resp.save()

    if "finished" in data:
        finish(id)


def finish(id):
    """Mark a SurveyResponse as finished

    Args:
        id (int): primary key of the surveyresponse to be returned
    """

    resp = SurveyResponse.get(SurveyResponse.id == id)
    error_msg = "Response ID {0} is missing field {1}; can't mark as finished"

    # If we are missing any mandatory fields, we can't finish out the response
    for field_name in ("name", "email", "age", "about_me"):
        field = getattr(resp, field_name, None)
        if field is None:
            raise RuntimeError(error_msg.format(resp.id, field_name))

    resp.finished = True
    resp.save()
