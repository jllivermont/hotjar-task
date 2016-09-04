import json

import falcon
from survey import domain
from survey.error import ValidationError


class NewSurveyResource(object):

    def on_post(self, req, resp):
        """Request to create a new survey response

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response

        Returns:
            201: Survey response created successfully
            400: Invalid/malformed request from client
            500: Server error
        """

        try:
            payload = json.loads(req.stream.read().decode("utf-8"))
            survey_response = domain.create_response(payload)

            if survey_response is not None:
                resp.status = falcon.HTTP_201
                resp.content_type = "application/json"
                resp.body = json.dumps({"id": survey_response.id})

        except ValidationError:
            resp.status = falcon.HTTP_400
        except Exception:
            resp.status = falcon.HTTP_500


class SurveyResource(object):

    def on_get(self, req, resp, id):
        """Get details of a survey response

        Args:
            req (falcon.Request): HTTP request
            resp (falcon.Response): HTTP response

        Returns:
            200: Survey response fetched successfully
            400: Invalid/malformed request from client
            500: Server error
        """

        try:
            id = req.get_param("id")
            survey_response = domain.get_response(id)

            if survey_response is not None:
                resp.status = falcon.HTTP_200
                resp.content_type = "application/json"
                resp.body = json.dumps(survey_response)

        except ValidationError:
            resp.status = falcon.HTTP_400
        except Exception:
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp, id):
        """Update an existing survey response"""
        pass
