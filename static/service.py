import falcon
import os


class StaticResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = self.content_type
        resp.set_headers({"Access-Control-Allow-Origin": "*"})

        path = os.path.join(os.environ["STATIC_CONTENT_PATH"], self.file_name)
        with open(path, 'r') as f:
            resp.body = f.read()


class LoaderResource(StaticResource):
    content_type = "application/json"
    file_name = "loader.js"


class WidgetResource(StaticResource):
    content_type = "text/html"
    file_name = "widget.html"


class StylesheetResource(StaticResource):
    content_type = "text/css"
    file_name = "stylesheet.css"
