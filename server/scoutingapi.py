import cherrypy
import os.path
import json

import server.model.schedule
import server.model.setup
import server.viewerapi
import server.scouting.tasks
import server.scouting.tablet
import server.scouting.sections
import server.model.match
import server.model.event
import server.scouting.load_data


class Scouting(object):
    def __init__(self):
        self.matchDal = server.model.match.MatchDal()
        self.eventDal = server.model.event.EventDal()
        self.alltablets = server.scouting.tablet.TabletList()

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
        return server.scouting.sections.Observers().load()

    @cherrypy.expose
    def gametasks(self):
        return server.scouting.tasks.TaskDal.csvtasks()

    @cherrypy.expose
    def matches(self, event='na'):
        if event == 'na':
            event = server.model.event.EventDal.get_current_event()

        return server.model.event.EventDal.list_matches(event)

    @cherrypy.expose
    def matchteams(self, match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        if match == 'na':
            return server.model.match.MatchDal.pit_teams()
        return server.model.match.MatchDal.match_teams(match)

    @cherrypy.expose
    def matchteamtasks(self, team='error', match=-1):
        if match == -1:
            match = self.eventDal.get_current_match()
        return (server.model.match.MatchDal.match_team_tasks(match, team) +
                '{end}')

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, capability=0, attempt=0,
                      success=0, cycle_time=0):
        try:
            server.model.match.MatchDal.insert_match_task(team, task, match,
                                                          phase, capability,
                                                          attempt, success,
                                                          cycle_time)
        except KeyError:
            return 'Error'
        return 'hi'

    @cherrypy.expose
    def tablet(self, status, ip=-1):
        newtablet = server.scouting.tablet.TabletDAL(status.split(':')[0],
                                                     status.split(':')[1], ip)

        if server.scouting.tablet.TabletList.settablet(self.alltablets,
                                                       newtablet):
            server.model.event.EventDal.set_next_match(
                self.eventDal.get_current_match())

        return self.eventDal.get_current_match()

    @cherrypy.expose
    def tablets(self):
        out = open("web/scripts/tablets.txt").read()
        out = self.alltablets.inserttablets(out)
        out = out.replace('{Match=""}',
                          '{Match="' + self.eventDal.get_current_match() + '"}')
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
        server.model.schedule.insert_sched(event, year, 'qual')
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def databaseset(self):
        server.model.setup.create_tables()
        server.model.setup.initialize_dimension_data()
        server.model.setup.load_game_sheet()
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def matchcreate(self, match, red1, red2, red3, blue1, blue2, blue3):
        return "successfully set match"

    @cherrypy.expose
    def matchenter(self, match=-1):
        out = open("web/sites/matchenter.html").read()
        schedule = self.matchteams(match).split('\n')
        redteams = json.loads(schedule[0])
        blueteams = json.loads(schedule[1])

        out.replace("{Red1}", redteams['team1'])
        out.replace("{Red2}", redteams['team2'])
        out.replace("{Red3}", redteams['team3'])
        out.replace("{Blue1}", blueteams['team1'])
        out.replace("{Blue2}", blueteams['team2'])
        out.replace("{Blue3}", blueteams['team3'])

        return out



if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})

    conf = {"/web": {'tools.staticdir.on': True,
                     'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.tree.mount(server.viewerapi.Viewer(False), '/view', config=conf)
    cherrypy.quickstart(Scouting(), '/', config=conf)
