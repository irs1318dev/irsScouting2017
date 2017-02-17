import cherrypy
import Game
# import Match


class Scouting(object):

    currentMatch = 1
    # def matchApi = new Match()

    def __init__(self):
        return

    @cherrypy.expose
    def index(self):
        return 'nothing to see here'

    @cherrypy.expose
    def games(self):
        return 'games'

    @cherrypy.expose
    def gamelayout(self):
        return Game.HelloWorld.game()
    # All tasks in layout

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
    def matchteams(self, match=currentMatch):
        return Game.HelloWorld.match(match)
    # All teams in match

    @cherrypy.expose
    def matchteam(self, match, team):
        return 'matchteam with match and team'

    @cherrypy.expose
    def matchteamtasks(self, team, match=currentMatch):
        return Game.HelloWorld.matchteam(match, team)
    # Get data from match and team

    @cherrypy.expose
    def matchteamtask(self, match, team, task, success=0, miss=0):
        Game.HelloWorld.data(match, team, task, success, miss)
        return 'put measure to system'

    @cherrypy.expose
    def dimensions(self):
        return 'dimensions'

    @cherrypy.expose
    def dimension(self, dimension):
        return 'dimension'

    @cherrypy.expose
    def tablet(self, status):
        return str(self.currentMatch)

    @cherrypy.expose
    def setmatch(self, match):
        self.currentMatch = match
        return 'set match'


if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Scouting())

