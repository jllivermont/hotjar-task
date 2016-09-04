import falcon

from survey.service import NewSurveyResource, SurveyResource


app = application = falcon.API()
app.add_route("/survey", NewSurveyResource())
app.add_route("/survey/{id}", SurveyResource())
