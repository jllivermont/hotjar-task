import requests

REQUEST_HEADERS = {"Content-Type": "application/json"}


# CREATE RESPONSE
def test_create_response_returns_201_on_success(test_webserver):
    input_dict = {"name": "Warren Buffet", "email": "oracle@omaha.com"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    assert resp.status_code == 201
    assert "id" in resp.json()


def test_create_response_returns_409_for_duplicate(test_webserver):
    input_dict = {"name": "Gene Hackman", "email": "gene@hackman.fr"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    assert resp.status_code == 201
    resp2 = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    assert resp2.status_code == 409
    expected_error = {'error': 'This user has already submitted a Survey'}
    assert resp2.json() == expected_error


def test_create_with_missing_attributes_returns_400(test_webserver):
    input_dict = {"name": "David Cameron"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    assert resp.status_code == 400
    expected_error = {'error': 'Missing mandatory field email'}
    assert resp.json() == expected_error


def test_improperly_formatted_email_returns_400(test_webserver):
    input_dict = {"name": "Joe Montana", "email": "123"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    assert resp.status_code == 400
    expected_error = {
        'error': 'Value for field email is not a valid email address'}
    assert resp.json() == expected_error


# GET RESPONSE
def test_get_response_with_non_integer_id_returns_400(test_webserver):
    resp = requests.get(test_webserver.url + "/survey/abcd")
    assert resp.status_code == 400
    expected_error = {'error': 'Specified ID is not a valid integer'}
    assert resp.json() == expected_error


def test_get_response_with_non_existant_id_returns_400(test_webserver):
    resp = requests.get(test_webserver.url + "/survey/23020932")
    assert resp.status_code == 400
    expected_error = {'error': 'Specified ID does not exist'}
    assert resp.json() == expected_error


def test_get_response_returns_200_on_success(test_webserver):
    input_dict = {"name": "Rory McIlroy", "email": "rory@pga.com"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    id = str(resp.json()["id"])

    resp = requests.get(test_webserver.url + "/survey/" + id)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Rory Mcilroy"
    assert resp.json()["email"] == "rory@pga.com"


# UPDATE RESPONSE
def test_update_response_with_non_existant_id_returns_400(test_webserver):
    update_dict = {"name": "babs bunny", "address": "4 Dame Lane"}
    resp = requests.put(
        url=test_webserver.url +
        "/survey/238298239",
        json=update_dict,
        headers=REQUEST_HEADERS)
    assert resp.status_code == 400
    assert resp.json() == {'error': 'Specified ID does not exist'}


def test_update_response_returns_200_on_success(test_webserver):
    # Create survey
    input_dict = {"name": "Freddy Krueger", "email": "jason@friday13.org"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    id = str(resp.json()["id"])

    # Update survey
    input_dict["name"] = "Jason Voorhees"
    input_dict["favorite_colors"] = " BLUE, green, BrOwN "
    del input_dict["email"]

    resp = requests.put(
        url=test_webserver.url +
        "/survey/" + id,
        json=input_dict,
        headers=REQUEST_HEADERS)

    assert resp.status_code == 200

    # Fetch and assert survey
    resp = requests.get(test_webserver.url + "/survey/" + id)
    updated_response = resp.json()
    assert resp.status_code == 200
    assert updated_response["name"] == "Jason Voorhees"
    assert updated_response["email"] == "jason@friday13.org"
    assert updated_response["favorite_colors"] == "blue,green,brown"


def test_update_response_with_email_returns_200(test_webserver):
    # Create survey
    input_dict = {"name": "Elmer Fudd", "email": "elmer@looney.org"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    id = str(resp.json()["id"])

    # Update survey
    input_dict["name"] = "Daffy Duck"
    input_dict["email"] = "daffy@looney.org"

    resp = requests.put(
        url=test_webserver.url +
        "/survey/" + id,
        json=input_dict,
        headers=REQUEST_HEADERS)

    # Fetch and assert survey
    resp = requests.get(test_webserver.url + "/survey/" + id)
    updated_response = resp.json()
    assert resp.status_code == 200
    assert updated_response["name"] == "Daffy Duck"
    assert updated_response["email"] == "daffy@looney.org"


def test_update_response_to_finish_unfinished_survey_returns_400(
        test_webserver):
    # Create survey
    input_dict = {"name": "Peter Parker", "email": "peter@marvel.com"}
    resp = requests.post(
        url=test_webserver.url +
        "/survey",
        json=input_dict,
        headers=REQUEST_HEADERS)
    id = str(resp.json()["id"])

    # Update survey
    input_dict["name"] = "Daffy Duck"
    input_dict["finished"] = "true"
    input_dict["about_me"] = "Flying kites"
    del input_dict["email"]

    resp = requests.put(
        url=test_webserver.url +
        "/survey/" + id,
        json=input_dict,
        headers=REQUEST_HEADERS)

    assert resp.status_code == 400
    assert "is missing field age; can't mark as finished" in resp.json()[
        "error"]


def test_get_all_responses_returns_200(test_webserver):
    resp = requests.get(url=test_webserver.url + "/surveys")

    assert resp.status_code == 200
    assert len(resp.json()) > 1
