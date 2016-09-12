import falcon
from static.service import Loader, Stylesheet, Survey, Test, Widget  # noqa
from survey.models import db_close, db_init
from survey.service import (AllSurveysResource, NewSurveyResource,  # noqa
                            SurveyResource)


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
app.add_route("/surveys", AllSurveysResource())

# Static content that we could/should serve from nginx
app.add_route("/loader.js", Loader())
app.add_route("/widget.html", Widget())
app.add_route("/survey.js", Survey())
app.add_route("/stylesheet.css", Stylesheet())
app.add_route("/test.html", Test())
