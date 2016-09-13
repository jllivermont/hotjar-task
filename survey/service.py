import json

import falcon
from peewee import IntegrityError
from survey.domain import (create_response, get_all_responses,  # noqa
                           get_response, update_response)
from survey.error import ValidationError
from survey.models import SurveyResponse
from survey.normalizer import normalize
from survey.notifier import notify
from survey.validator import validate


def _decode(req, resp):
    try:
        return json.loads(req.stream.read().decode("utf-8"))
    except Exception:
        resp.body = json.dumps({"error": "Unable to decode request payload"})
        resp.status = falcon.HTTP_500


def _validate(data, resp, mandatory_fields=None, forbidden_fields=None):
    try:
        data = normalize(data)
        validate(data, mandatory_fields, forbidden_fields)
        return data
    except ValidationError as e:
        resp.body = json.dumps({"error": e.args[0]})
        resp.status = falcon.HTTP_400
    except Exception as e:
        msg = "Unable to validate request payload: {}".format(e.args[0])
        resp.body = json.dumps({"error": msg})
        resp.status = falcon.HTTP_400


def _get_id(id, resp):
    try:
        return int(id)
    except Exception:
        resp.body = json.dumps(
            {"error": "Specified ID is not a valid integer"})
        resp.status = falcon.HTTP_400


class NewSurveyResource(object):

    def on_post(self, req, resp):
        """Request to create a new survey response

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response

        Returns:
            201: Survey response created successfully
            400: Invalid/malformed request from client
            409: Resource already exists (violation of uniqueness constraints)
            500: Server error
        """

        resp.content_type = "application/json"
        resp.status = falcon.HTTP_201

        # Decode the request payload
        data = _decode(req, resp)
        if data is not None:
            # Normalize and validate the input data
            mandatory_fields = ("name", "email")
            data = _validate(data, resp, mandatory_fields=mandatory_fields)

        if resp.status == falcon.HTTP_201:
            try:
                id = create_response(data)
                resp.body = json.dumps({"id": id})
                notify("create", json.dumps(get_response(id)))
            except IntegrityError:
                resp.body = json.dumps(
                    {"error": "This user has already submitted a Survey"})
                resp.status = falcon.HTTP_409
            except Exception:
                resp.body = json.dumps({"error": "Unable to persist response"})
                resp.status = falcon.HTTP_500


class SurveyResource(object):

    def on_get(self, req, resp, id):
        """Get details of a survey response

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response
            id (int): Primary key of row to return

        Returns:
            200: Survey response fetched successfully
            400: Invalid/malformed request from client
            500: Server error
        """

        resp.content_type = "application/json"

        id = _get_id(id, resp)
        if id is not None:
            try:
                survey_response = get_response(id)

                if survey_response is not None:
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps(survey_response)
                else:
                    raise RuntimeError()
            except SurveyResponse.DoesNotExist:
                resp.body = json.dumps(
                    {"error": "Specified ID does not exist"})
                resp.status = falcon.HTTP_400
            except Exception:
                resp.body = json.dumps(
                    {"error": "Unable to fetch response from persistence"})
                resp.status = falcon.HTTP_500

    def on_put(self, req, resp, id):
        """Request to update an existing survey response

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response

        Returns:
            200: Survey response updated successfully
            400: Invalid/malformed request from client
            500: Server error
        """

        resp.status = falcon.HTTP_200

        id = _get_id(id, resp)
        if id is not None:
            # Decode the request payload
            data = _decode(req, resp)
            if data is not None:
                # Normalize and validate the input data
                forbidden_fields = ("email",)
                data = _validate(data, resp, forbidden_fields=forbidden_fields)

        if resp.status == falcon.HTTP_200:
            try:
                update_response(id, data)
                notify("update", json.dumps(get_response(id)))
            except SurveyResponse.DoesNotExist:
                resp.body = json.dumps(
                    {"error": "Specified ID does not exist"})
                resp.status = falcon.HTTP_400
            except RuntimeError as e:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({"error": e.args[0]})
            except Exception:
                resp.status = falcon.HTTP_500
                resp.body = json.dumps(
                    {"error": "Unable to persist updated response"})


class AllSurveysResource(object):

    def on_get(self, req, resp):
        """Get details of all survey responses

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response

        Returns:
            200: Survey response fetched successfully
            400: Invalid/malformed request from client
            500: Server error
        """

        resp.content_type = "application/json"

        try:
            survey_response = get_all_responses()
            if survey_response is not None:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(survey_response)
            else:
                raise RuntimeError()
        except Exception:
            resp.body = json.dumps(
                {"error": "Unable to fetch responses from persistence"})
            resp.status = falcon.HTTP_500
