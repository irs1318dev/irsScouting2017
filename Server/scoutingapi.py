import cherrypy
import Game
import scouting.tablet
import scouting.sections

import scouting.match


class Scouting(object):
    currentMatch = 1
    maxMatch = 2

    def __init__(self):
        self.matchDal = scouting.match.MatchDal()
        return

    @cherrypy.expose
    def index(self):
        return 'nothing to see here'

    @cherrypy.expose
    def games(self):
        return 'games'

    @cherrypy.expose
    def gamelayout(self):
        return scouting.sections.Observers().load()

    @cherrypy.expose
    def gametasks(self):
        return Game.HelloWorld.gametasks()

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
    def matchteams(self, match='hi'):
        if match is 'hi':
            match = self.currentMatch
        return Game.HelloWorld.match(match)

    # All teams in match

    @cherrypy.expose
    def matchteam(self, match, team):
        return 'matchteam with match and team'

    @cherrypy.expose
    def matchteamtasks(self, team, match=-1, phase='claim'):
        if match == -1:
            match = self.currentMatch
        #return scouting.match.MatchDal.matchteamtasks(match, team, phase)
            return '{}'

    # Get data from match and team

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, success=0, miss=0):
        # return scouting.match.MatchDal.matchteamtask(match, team, task, phase, success, miss)
        return 'Temp fix here'

    @cherrypy.expose
    def dimensions(self):
        return 'dimensions'

    @cherrypy.expose
    def dimension(self, dimension):
        return 'dimension'

    # Completed functions here on
    # __________________________________________________________________________

    alltablets = list({scouting.tablet.TabletDAL('TestSystem', 'Waiting')})

    @cherrypy.expose
    def tablet(self, status):
        newtablet = scouting.tablet.TabletDAL(status.split(':')[0], status.split(':')[1])
        found = False
        nextmatch = True
        i = 0

        while i < len(self.alltablets):
            if self.alltablets[i].position in newtablet.position:
                self.alltablets[i].page = newtablet.page
                found = True
            if 'Waiting' not in self.alltablets[i].page:
                nextmatch = False
            i += 1

        if not found:
            self.alltablets.append(newtablet)
            if 'Waiting' not in newtablet.page:
                nextmatch = False

        if nextmatch:
            if self.currentMatch < self.maxMatch:
                self.currentMatch += 1

        return str(self.currentMatch)

    @cherrypy.expose
    def tablets(self):
        s = ""

        for tab in self.alltablets:
            s += tab.write()

        return s

    @cherrypy.expose
    def matchcurrent(self, match):
        self.currentMatch = match
        return 'set match'


if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Scouting())
