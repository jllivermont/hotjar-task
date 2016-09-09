import falcon
from survey.models import db_close, db_init
from survey.service import NewSurveyResource, SurveyResource, LoaderResource, WidgetResource, StylesheetResource  # noqa
from static.service import LoaderResource, WidgetResource, StylesheetResource  # noqa 


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

# Static content that we could/should serve from nginx
app.add_route("/loader", LoaderResource())
app.add_route("/widget", WidgetResource())
app.add_route("/stylesheet", StylesheetResource())

