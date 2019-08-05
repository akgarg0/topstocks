import cherrypy
import cherryServer
import os

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
    cherrypy.quickstart(cherryServer.CherryServer(), '/', conf)
    print('Deployed')
