from survey.normalizer import normalize


def test_fields():
    input_data = {
        "name": " steve jobs",
        "email": "steve @blue.org ",
        "age": "52 ",
        "about_me": " I love fish!! !",
        "address": "N/A",
        "gender": " MALE",
        "favorite_book": "Call of the Wild ",
        "favorite_colors": " RED, pINK , blue  "
    }

    normalized_data = normalize(input_data)

    assert normalized_data["name"] == "Steve Jobs"
    assert normalized_data["email"] == "steve@blue.org"
    assert normalized_data["age"] == 52
    assert normalized_data["about_me"] == "I love fish!! !"
    assert normalized_data["address"] == "N/A"
    assert normalized_data["gender"] == "male"
    assert normalized_data["favorite_book"] == "Call of the Wild"
    assert normalized_data["favorite_colors"] == "red,pink,blue"
