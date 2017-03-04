import cherrypy
import Game
import scouting.tasks
import scouting.tablet
import scouting.sections
import scouting.match
import scouting.event


class Scouting(object):
    def __init__(self):
        self.matchDal = scouting.match.MatchDal()
        self.eventDal = scouting.event.EventDal()
        self.alltablets = scouting.tablet.TabletList()
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
        return scouting.tasks.TaskDal.csvtasks()

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
    def matchteams(self, match=-1):
        if match == -1:
            match = '001-q'
        # return self.eventDal.match_teams(self.eventDal.getCurrentEvent(), self.eventDal.getCurrentMatch())
        return Game.HelloWorld.match(match)

    # All teams in match

    @cherrypy.expose
    def matchteam(self, match, team):
        return 'matchteam with match and team'

    @cherrypy.expose
    def matchteamtasks(self, team, match=-1, phase='claim'):
        if match == -1:
            match = self.eventDal.getCurrentMatch()
        # return scouting.match.MatchDal.matchteamtasks(match, team, phase)
        return '{}'

    # Get data from match and team

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, capability=0, attempt=0, success=0, cycle_time=0):
        scouting.match.MatchDal.matchteamtask(match, team, task, phase, capability, attempt, success, cycle_time)
        return 'hi'

    @cherrypy.expose
    def dimensions(self):
        return 'dimensions'

    @cherrypy.expose
    def dimension(self, dimension):
        return 'dimension'

    @cherrypy.expose
    def tablet(self, status):
        newtablet = scouting.tablet.TabletDAL(status.split(':')[0], status.split(':')[1])

        if scouting.tablet.TabletList.settablet(self.alltablets, newtablet):
            scouting.event.EventDal.setCurrentMatch()

        return self.eventDal.getCurrentMatch()

    @cherrypy.expose
    def tablets(self):
        return scouting.tablet.TabletList.gettablets(self.alltablets)

    @cherrypy.expose
    def matchcurrent(self, match):
        self.eventDal.setCurrentMatch(match)
        return 'set match'


if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Scouting())
