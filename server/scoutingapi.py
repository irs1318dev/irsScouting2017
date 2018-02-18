import cherrypy
import os.path
import json

import server.config as s_config
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
        """Returns Scouting System start page.

        Start page displays current match and event, allows user to set
        current match, displays a table showing tablet pages, and includes
        links to other scouting system pages.

        Returns: (str) HTML text
        """
        out = open(s_config.web_sites("admin.html")).read()
        out = out.replace('{Match}', self.eventDal.get_current_match())
        out = out.replace('{Event}', self.eventDal.get_current_event()[1])
        out = out.replace('{Year}', self.eventDal.get_current_event()[2])
        return out

    @cherrypy.expose
    def setup(self):
        """Returns Scouting System setup page.

        Allows user to set event and contains links for server
        directions, entering the schedule manually, setting up a new
        database, and backing up data.

        Returns: (str) HTML text
        """
        out = open(s_config.web_sites("setup.html")).read()
        out = out.replace('{Event}', self.eventDal.get_current_event()[1])
        out = out.replace('{Year}', self.eventDal.get_current_event()[2])
        return out

    @cherrypy.expose
    def gamelayout(self):
        """Returns pseudo-JSON string with season-specific tasks

        Data formatted as JSON list of key-value objects.

        JSON keys:
            actor: Entity that completes task, such as robot, alliance,
            or team.
            category: Examples include Starting, Gear, Fuel, Climb, etc.
            newpart: true or false. Not sure what this is.
            observer: Where task is observed, such as match or pit.
            phase: Part of competition in which task occurs, such as
            auto, teleop, claim, or finish.
            position: "", 1, 2, 3, or waiting.
            tasks: Name of task, such as placeGear or pushTouchPad

        Returns: (str) pseudo-JSON text. The individual JSON
        dictionaries are separated by "\n" carriage return characters
        instead of being separated by commas and included in a list.
        """
        return server.scouting.sections.Observers().load()

    @cherrypy.expose
    def gametasks(self):
        """Returns pseudo-JSON string with season specific tasks

        JSON keys:
            actor: Entity that completes task, such as robot, alliance,
            or team.
            auto: datatype or "na" if task does not apply to auto
            claim: datatype or "na" if task does not apply to claim
            enums: Used when tablet UI displays a drop-down list for
                data entry. Contains list of options separated by '|',
                or "" empty string if drop-down list not used.
            finish: datatype or "na" if task does not apply to claim
            miss: ???
            success: ???
            task: name of task, such as placeGear or shootLowBoiler
            teleop: datatype or "na" if task does not apply to teleop

        Returns: (str) pseudo-JSON text. The individual JSON
        dictionaries are separated by "\n" carriage return characters
        instead of being separated by commas and included in a list.
        """
        return server.scouting.tasks.TaskDal.csvtasks()

    @cherrypy.expose
    def matches(self, event='na'):
        """Returns JSON list of matches.

        Args:
            event: The FIRST API event code.

        Returns: List contains 1 dictionary for each match. Each
        dictionary contains two keys: "match" and "event".
        """
        if event == 'na':
            event = server.model.event.EventDal.get_current_event()

        return server.model.event.EventDal.list_matches(event[1],
                                                        event[2])

    @cherrypy.expose
    def matchteams(self, match=-1):
        """Gets string with teams assigned to match or competition.

        Args:
            match:
                (str) Can be set to -1 (default), "na", or to a
                match number, e.g., "001-q". Optional.

                If set to -1, returns team from current match specified
                in status table in database server. Eacha lliance will
                be a JSON string, with alliances separated by carriage
                returns ("\n"). The JSON string keys are "alliance"
                ("red" or "blue"), "match", "team1", "team2", and
                "team3".

                If set to a match number, ignores current match
                specified in status table and returns teams assigned
                to match number. The format of resulting test string
                is the same as if -1 is specified.

                If set to "na", returns a Python dictionary. The "match"
                key contains "na" and the "teams" key contains a list of
                FRC team numbers as strings, as well as the value "na".

        Returns: pseudo-JSON string or JSON string representing a
        Python dictionary.
        """
        if match == -1:
            match = self.eventDal.get_current_match()
        if match == 'na':
            return server.model.match.MatchDal.pit_teams()
        return server.model.match.MatchDal.match_teams(match)

    @cherrypy.expose
    def matchteamtasks(self, team='error', match=-1):
        """ Returns measures for a single team in a single match

        Args:
            team: (str) FRC team number
            match: Competitiion match number, such as "001-q"

        Returns: (str) Pseudo JSON code. Measures are separated by
        carriage returns ("\n") and dach measure is a JSON object
        literal with keys "match", "team", "task", "phase", "actor",
        "measuretype", "capability", "attempts", "success", and
        "cycle_times".

        """
        if match == -1:
            match = self.eventDal.get_current_match()
        return (server.model.match.MatchDal.match_team_tasks(match, team) +
                '{end}')

    @cherrypy.expose
    def matchteamtask(self, match, team, task, phase, capability='', attempt=0,
                      success=0, cycle_time=0):
        """Writes a measure to the database.

        Args:
            match: (str) Match number, such as "007-q".
            team: (str) FRC team number
            task: (str) Task name (season specific) such as "placeGear"
            phase: (str) Portion of competition to which task applies,
                such as "claim", "auto", "teleop", etc,
            capability: "true" if task just records that team or robot
                has a capability to do something (may be used in pit
                scouting).
            attempt: (int) Number of attempts made to complete this
                task, successful or not.
            success: (int) Number of successful attempts made to
                complete this task.
            cycle_time: (int) Amount of time required to complete a
                task, in seconds.

        Returns: (str) "hi"
        """
        try:
            server.model.match.MatchDal.insert_match_task(team, task, match,
                                                          phase, capability,
                                                          attempt, success,
                                                          cycle_time)
        except KeyError as key:
            return 'KeyError: ' + str(key)
        return 'hi'

    @cherrypy.expose
    def tablet(self, status, ip=-1):
        newtablet = server.scouting.tablet.TabletDAL(status.split(':')[0], status.split(':')[1], ip)

        if server.scouting.tablet.TabletList.settablet(self.alltablets, newtablet):
            server.model.event.EventDal.set_next_match(self.eventDal.get_current_match())

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
    def eventcurrent(self, event, year):
        self.eventDal.set_current_event(event, year)
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def eventfind(self, event, year):
        self.eventDal.set_current_event(event, year)
        self.eventDal.set_current_match('001-q')
        server.model.schedule.insert_sched(event, year, 'qual')
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def addresslist(self):
        return self.alltablets.get_address();

    @cherrypy.expose
    def databaseset(self):
        server.model.setup.setup()
        return open("web/sites/reset.html").read()



if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})

    conf = {"/web": {'tools.staticdir.on': True,
                     'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.tree.mount(server.viewerapi.Viewer(False), '/view', config=conf)
    cherrypy.quickstart(Scouting(), '/', config=conf)
