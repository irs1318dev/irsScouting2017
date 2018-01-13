import cherrypy
import firstapi

class MatchResults(object):
    @cherrypy.expose
    def result(self):
        return firstapi.getMatchResults('WAAMV', '2017', '33', 'qual')


class MatchScores(object):
    @cherrypy.expose
    def result(self):
        return firstapi.getMatchScores('WAAMV', '2017', 'qual')

cherrypy.quickstart(MatchResults())