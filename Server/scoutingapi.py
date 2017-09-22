import cherrypy
import os.path
import viewerapi
import scouting.tasks
import scouting.tablet
import scouting.sections
import scouting.match
import scouting.event
import scouting.load_data


class Scouting(object):
    def __init__(self):
        self.matchDal = scouting.match.MatchDal()
        self.eventDal = scouting.event.EventDal()
        self.alltablets = scouting.tablet.TabletList()

    @cherrypy.expose
    def index(self):
        out = open("web/sites/admin.html").read()
        out = out.replace('{Match}', self.eventDal.get_current_match())
        out = out.replace('{Event}', self.eventDal.get_current_event())
        return out

    @cherrypy.expose
    def setup(self):
        out = open("web/sites/setup.html").read()
        out = out.replace('{Event}', self.eventDal.get_current_event())
        return out

    @cherrypy.expose
    def gamelayout(self):
        return scouting.sections.Observers().load()

    @cherrypy.expose
    def gametasks(self):
        return scouting.tasks.TaskDal.csvtasks()

    @cherrypy.expose
    def matches(self, event='na'):
        if event == 'na':
            event = scouting.event.EventDal.get_current_event()

        return scouting.event.EventDal.list_matches(event)

    @cherrypy.expose
    def matchteams(self, match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        if match == 'na':
            return scouting.match.MatchDal.pitteams()
        return scouting.match.MatchDal.matchteams(match)

    @cherrypy.expose
    def matchteamtasks(self, team='error', match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        return scouting.match.MatchDal.matchteamtasks(match, team) + '{end}'

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, capability=0, attempt=0, success=0, cycle_time=0):
        try:
            scouting.match.MatchDal.matchteamtask(team, task, match, phase, capability, attempt, success, cycle_time)
        except KeyError:
            return 'Error'
        return 'hi'

    @cherrypy.expose
    def tablet(self, status, ip=-1):
        newtablet = scouting.tablet.TabletDAL(status.split(':')[0], status.split(':')[1], ip)

        if scouting.tablet.TabletList.settablet(self.alltablets, newtablet):
            scouting.event.EventDal.set_next_match(self.eventDal.get_current_match())

        return self.eventDal.get_current_match()

    @cherrypy.expose
    def tablets(self):
        out = open("web/scripts/tablets.txt").read()
        out = self.alltablets.inserttablets(out)
        out = out.replace('{Match=""}', '{Match="' + self.eventDal.get_current_match() + '"}')
        return out

    @cherrypy.expose
    def matchcurrent(self, match):
        self.tablet('TestSystem:Reset')
        self.eventDal.set_current_match(match)
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def eventcurrent(self, event):
        self.eventDal.set_current_event(event)
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def eventfind(self, event, year='2017'):
        self.eventDal.set_current_event(event)
        self.eventDal.set_current_match('001-q')
        scouting.load_data.insert_sched(event, year, 'qual')
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def databaseset(self):
        scouting.db.create_tables()
        scouting.db_dimensiondata.insert_data()
        scouting.load_data.load_game_sheet()
        return open("web/sites/reset.html").read()

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})

    conf = {"/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.tree.mount(viewerapi.Viewer(False), '/view', config=conf)
    cherrypy.quickstart(Scouting(), '/', config=conf)
