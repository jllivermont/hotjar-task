import falcon
import json


class NewSurveyResource(object):
    def on_post(self, req, resp):
        req_payload = json.loads(req.stream.read().decode("utf-8"))
        req_payload["name"] = "james"
        resp.body = json.dumps(req_payload)
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200


class SurveyResource(object):
    def on_get(self, req, resp, id):
        id = req.get_param("id")
        resp.data = id
        resp.content_type = 'test/plain'
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, id):
        pass


app = application = falcon.API()
app.add_route("/survey", NewSurveyResource())
app.add_route("/survey/{id}", SurveyResource())
