import cherrypy
import firstapi

class MatchResults(object):
    @cherrypy.expose
    def result(self):
        return firstapi.getMatchResults('WAAMV', '2017', '33', 'qual')

cherrypy.quickstart(MatchResults())