import cherrypy
from mako.template import Template
import os

import stocks
import parseFile
import database


@cherrypy.expose
class CherryServer:
    @cherrypy.tools.accept(media='text/html')
    def GET(self):
        red = database.DataBase()
        data = red.get_top_10_or_searched()
        headers = parseFile.DEFAULT_FIELDS.values()
        print(data)
        print(headers)
        return Template(filename="public/ListSearch.html").render(data=data, headers=headers)

    def POST(self, name=''):
        red = database.DataBase()
        data = red.get_top_10_or_searched(name)
        headers = parseFile.DEFAULT_FIELDS.values()
        return Template(filename="public/ListSearch.html").render(data=data, headers=headers)

    def PUT(self, another_string):
        path = 'tmp'
        for root, dirs, files in os.walk(path):
            for file in files:
                path = os.path.join(path, file)
                os.remove(path)
        bc = stocks.BhavCopy()
        bc.download_zip()
        red = database.DataBase()
        red.delete_all()
        red.load_csv_to_db()
        return "New Data Fetched Successfully"

    def DELETE(self):
        red = database.DataBase()
        red.delete_all()
        return "Data Deleted Successfully"


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        }
    }
    cherrypy.quickstart(CherryServer(), '/', conf)
