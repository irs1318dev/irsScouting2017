import cherrypy
import firstapi


class Schedule(object):
    @cherrypy.expose
    def index(self):
        return firstapi.getSched('WAAMV', '2017')

    @cherrypy.expose
    def sched(self, event):
        return firstapi.getSched(event, '2017')

cherrypy.quickstart(Schedule())
