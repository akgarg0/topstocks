import cherrypy
from mako.template import Template
import os

import stocks
import parseFile
import database


@cherrypy.expose
class CherryServer:
    def common(self, name=""):
        red = database.DataBase()
        data = red.get_top_10_or_searched(name)
        headers = parseFile.DEFAULT_FIELDS.values()
        return Template(filename="public/ListSearch.html").render(data=data, headers=headers)

    @cherrypy.tools.accept(media='text/html')
    def GET(self):
        return self.common()

    def POST(self, name='', _method=''):
        if _method == 'put':
            return self.PUT()
        elif _method == 'delete':
            return self.DELETE()
        return self.common(name)

    def PUT(self):
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
        return self.common()

    def DELETE(self):
        red = database.DataBase()
        red.delete_all()
        return self.common()


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath("public/css")
        },
    }
    cherrypy.quickstart(CherryServer(), '/', conf)
