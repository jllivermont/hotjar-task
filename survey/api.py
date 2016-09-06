import falcon
from survey.models import db_close, db_init
from survey.service import NewSurveyResource, SurveyResource


class DBConnectionManager(object):
    # Initialize a connection prior to routing
    def process_request(self, req, resp):
        db_init()

    # Close the connection after the request has been serviced
    def process_response(self, req, resp, resource):
        db_close()

app = application = falcon.API(middleware=[
    DBConnectionManager(),
])

app.add_route("/survey", NewSurveyResource())
app.add_route("/survey/{id}", SurveyResource())
app.add_route("/survey/{id}/finish", SurveyResource())