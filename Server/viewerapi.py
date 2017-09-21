import cherrypy
from cherrypy.lib.static import serve_file
import os.path
import scouting.export
import scouting.output
import scouting.event
import scouting.alliance
import scouting.match


class Viewer:
    def __init__(self, alone=True):
        self.alone = alone
        self.alliances = scouting.alliance.AlliancePage()
        self.export = scouting.export.ExportBackup

    @cherrypy.expose
    def index(self):
        out = open('web/sites/view.html').read()

        if self.alone:
            out = out.replace('{Back}', '')
        else:
            out = out.replace('{Back}', '<h3><a href="/">Scouting Director</a></h3>')

        return out

    @cherrypy.expose
    def data(self, name):
        name = os.path.abspath('web/data/') + '/' + name
        if os.path.exists(name):
            return serve_file(name, "application/x-download", "attachment")
        return 'No File Found'

    @cherrypy.expose
    def output(self):
        excel = scouting.output.get_Path('Report')
        scouting.output.get_report(excel)
        return '<a href="/view/data?name=' + excel + '">Download File</a>'
        # return open("web/resetView.html").read()

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

        out = open("web/sites/selection.html").read()
        out = out.replace("{Unset}", self.alliances.unset())
        out = self.alliances.selections(out)
        return out

    @cherrypy.expose
    def backup(self):
        script = self.export.run_backup(scouting.event.EventDal.get_current_event())
        return '<a href="/view/data?name=' + script + '">Download File</a>'

    @cherrypy.expose
    def restore(self, path):
        self.export.run_restore(path)
        return open("web/sites/reset.html").read()

    @cherrypy.expose
    def teamplan(self, team='1318'):
        match = '001-q'
        matches = list()

        while '""' not in scouting.match.MatchDal.matchteams(match) and '130' not in match:
            if team in scouting.match.MatchDal.matchteams(match):
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

        while True:
            nextMatchNumber = int(match.split('-')[0]) - 1
            if nextMatchNumber > 0:
                match = "{0:0>3}-q".format(nextMatchNumber)

                for team in nextMatch:
                    if team in self.teamsList(match):
                        return setMatch + ' : ' + str(self.teamsList(setMatch)) + ' After ' + match

    def teamsList(self, match):
        teams = list()
        for data in scouting.match.MatchDal.matchteams(match).split(','):
            if 'team' in data:
                teams.append(data.split(':')[1].split('"')[1])
        return teams


class Start:
    @cherrypy.expose
    def index(self):
        return open("web/sites/resetView.html")

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 1318})
    conf = {"/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.tree.mount(Viewer(), '/view', config=conf)
    cherrypy.quickstart(Start(), '/')
