import cherrypy
import os
import viewerapi
import scouting.tasks
import scouting.tablet
import scouting.sections
import scouting.match
import scouting.event
import scouting.export
import scouting.output


class Scouting(object):
    def __init__(self):
        self.matchDal = scouting.match.MatchDal()
        self.eventDal = scouting.event.EventDal()
        self.alltablets = scouting.tablet.TabletList()

    @cherrypy.expose
    def index(self):
        out = open("web/admin.html").read()
        out = out.replace('{Match}', self.eventDal.get_current_match())
        out = out.replace('{Event}', self.eventDal.get_current_event())
        out = self.alltablets.inserttablets(out)
        return out

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
    def status(self):
        return scouting.event.EventDal.get_current_status()

    @cherrypy.expose
    def events(self):
        return scouting.event.EventDal.list_events()

    @cherrypy.expose
    def matches(self, event='na'):
        if event == 'na':
            event = scouting.event.EventDal.get_current_event()

        return scouting.event.EventDal.list_matches(event)

    #        return matchApi.matches()

    @cherrypy.expose
    def match(self, match):
        return scouting.event.EventDal.set_current_match(match)

    @cherrypy.expose
    def matchteams(self, match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        if match == 'na':
            return scouting.match.MatchDal.pitteams()
        return scouting.match.MatchDal.matchteams(match)

    # All teams in match

    @cherrypy.expose
    def matchteam(self, match, team):
        return 'matchteam with match and team'

    @cherrypy.expose
    def matchteamtasks(self, team='error', match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        return scouting.match.MatchDal.matchteamtasks(match, team) + '{end}'

    # Get data from match and team

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, capability=0, attempt=0, success=0, cycle_time=0):
        try:
            scouting.match.MatchDal.matchteamtask(team, task, match, phase, capability, attempt, success, cycle_time)
        except KeyError:
            return 'Error'
        return 'hi'

    @cherrypy.expose
    def dimensions(self):
        return 'dimensions'

    @cherrypy.expose
    def dimension(self, dimension):
        return 'dimension'

    @cherrypy.expose
    def tablet(self, status, ip=-1):
        newtablet = scouting.tablet.TabletDAL(status.split(':')[0], status.split(':')[1], ip)

        if scouting.tablet.TabletList.settablet(self.alltablets, newtablet):
            scouting.event.EventDal.set_next_match(self.eventDal.get_current_match())

        return self.eventDal.get_current_match()

    @cherrypy.expose
    def tablets(self):
        return self.alltablets.gettablets()

    @cherrypy.expose
    def matchcurrent(self, match):
        self.tablet('TestSystem:Reset')
        self.eventDal.set_current_match(match)
        return open("web/reset.html").read()

    @cherrypy.expose
    def eventcurrent(self, event):
        scouting.event.EventDal.set_current_event(event)
        return open("web/reset.html").read()

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})

    conf = {"/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.tree.mount(viewerapi.Viewer(False), '/view', config=conf)
    cherrypy.quickstart(Scouting(), '/', config=conf)
