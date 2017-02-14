import cherrypy
import firstapi


class Schedule(object):
    @cherrypy.expose
    def index(self):
        return firstapi.getSched('WAAMV', '2016')

    @cherrypy.expose
    def sched(self, event):
        return firstapi.getSched(event, '2016')

cherrypy.config.update(
    {'server.socket_port': 1318})
cherrypy.quickstart(Schedule())
