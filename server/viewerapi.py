import cherrypy
from cherrypy.lib.static import serve_file
import os.path
import server.config as s_config
import server.scouting.export
import server.model.event as event
import server.scouting.alliance
import server.model.match as match
import server.view.graphing as graphing
import server.view.excel as excel
import server.scouting.export as export


class Viewer:
    def __init__(self, alone=True):
        self.alone = alone
        self.alliances = server.scouting.alliance.AlliancePage()

    @cherrypy.expose
    def index(self):
        out = open(s_config.web_sites("view.html")).read()

        if self.alone:
            out = out.replace('{Back}', '')
        else:
            out = out.replace('{Back}', '<h3><a href="/">Scouting Director</a></h3>')
        out = out.replace('{Match}', event.EventDal.get_current_match())

        return out

    @cherrypy.expose
    def data(self, name):
        name = s_config.web_data("name")
        if os.path.exists(name):
            return serve_file(name, "application/x-download", "attachment")
        return 'No File Found'

    @cherrypy.expose
    def selection(self, team='', index=-1, shift=-1, out=False):
        self.alliances.start()
        if team != '':
            self.alliances.alliances.set(team)
        if index != -1:
            self.alliances.alliances.choose(index)
        if shift != -1:
            self.alliances.shift(shift)
        if out:
            self.alliances.alliances.output()

        out = open(s_config.web_sites("selection.html")).read()
        out = out.replace("{Unset}", self.alliances.unset())
        out = self.alliances.selections(out)
        return out

    @cherrypy.expose
    def backup(self):
        script = export.ExportBackup.run_backup(
            server.model.event.EventDal.get_current_event()[1])
        return '<a href="/view/data?name=' + script + '">Download File</a>'

    @cherrypy.expose
    def output(self):
        script = ''
        script = excel.write_to_excel()
        return '<a href="/view/data?name=' + script + '">Download File</a>'

    @cherrypy.expose
    def restore(self, path):
        self.export.run_restore(path)
        return open(s_config.web_sites("reset.html")).read()

    @cherrypy.expose
    def eventplan(self):
        graphing.graph_event()
        return open(s_config.web_data('eventData.html')).read() 

    @cherrypy.expose
    def teamplan(self, team='1318'):
        match = '001-q'
        matches = list()

        while '""' not in server.model.match.MatchDal.match_teams(match) and '130' not in match:
            if team in server.model.match.MatchDal.match_teams(match):
                matches.append(match)

            nextMatchNumber = int(match.split('-')[0]) + 1
            match = "{0:0>3}-q".format(nextMatchNumber)

        out = ''
        for match in matches:
            out += '<a href="matchplan?match={M}">{M}</a> '
            out = out.replace('{M}', match)
        return out

    @cherrypy.expose
    def matchplan(self, match):
        nextMatch = self.teamsList(match)
        setMatch = match
        running = True
        out = open(s_config.web_sites('graphing.html')).read()
        out = out.replace('{Match}', match)
        out = out.replace('{Schedule}', setMatch + ' : ' + str(self.teamsList(setMatch)))

        while running:
            nextMatchNumber = int(match.split('-')[0]) - 1
            if nextMatchNumber > 0:
                match = "{0:0>3}-q".format(nextMatchNumber)

                for team in nextMatch:
                    if team in self.teamsList(match):
                        running = False
                        out =  out.replace('{After}', 'Final After: ' + match + ' Updated: ' + event.EventDal.get_current_match())
            else:
                running = False
                out =  out.replace('{After}', 'Updated: ' + event.EventDal.get_current_match())

        graphing.graph_match(self.teamsList(setMatch))
        return out.replace('{Data}', open(s_config.web_data('matchData.html')).read()) 

    @cherrypy.expose
    def customplan(self, red1, red2, red3, blue1, blue2, blue3):
        out = open(s_config.web_sites('graphing.html')).read()
        teams = [red1, red2, red3, blue1, blue2, blue3]
        out = out.replace('{Match}', 'Custom')
        out = out.replace('{Schedule}', str(teams))
        out = out.replace('{After}', 'Updated: ' + event.EventDal.get_current_match())

        graphing.graph_match(teams)
        return out.replace('{Data}', open(s_config.web_data('matchData.html')).read()) 


    def teamsList(self, match):
        teams = list()
        for data in server.model.match.MatchDal.match_teams(match).split(','):
            if 'team' in data:
                teams.append(data.split(':')[1].split('"')[1])
        return teams


class Start:
    @cherrypy.expose
    def index(self):
        return open(s_config.web_sites("resetView.html"))

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 1318})
    conf = {"/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': s_config.web_base()}}

    cherrypy.tree.mount(Viewer(), '/view', config=conf)
    cherrypy.quickstart(Start(), '/')
