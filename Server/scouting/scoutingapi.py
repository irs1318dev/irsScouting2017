import cherrypy
#import Match

class Scouting(object):

#   def matchApi = new Match()

    def __init__(self):
        return

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name

    @cherrypy.expose
    def games(self):
        return 'games'

    @cherrypy.expose
    def gamelayout(self):
        return 'gamelayout'

    @cherrypy.expose
    def gameimport(self):
        return 'gameimport'

    @cherrypy.expose
    def events(self):
        return 'event'

    @cherrypy.expose
    def event(self, event):
       return 'event with id'


    @cherrypy.expose
    def matches(self):
        return 'matches'
#        return matchApi.matches()

    @cherrypy.expose
    def match(self, match):
        return 'match with id'

    @cherrypy.expose
    def matchteams(self,match):
        return 'matchteam with match'

    @cherrypy.expose
    def matchteam(self, match, team):
        return 'matchteam with match and team'

    @cherrypy.expose
    def matchteamtasks(self, match, team):
        return 'matchteamtask with match and team'

    @cherrypy.expose
    def matchteamtask(self, match, team, task):
        return 'matchteamtask with match, team and task'

    @cherrypy.expose
    def dimensions(self):
        return 'dimensions'

    @cherrypy.expose
    def dimension(self, dimension):
        return 'dimension'









if __name__ == '__main__':
    cherrypy.quickstart(Scouting())
