import cherrypy
from cherrypy.lib.static import serve_file
import os.path
import server.config as s_config
import server.scouting.export
import server.model.event as event
import server.model.match as match
import server.season.s2018.viewer as graphing
import server.view.excel as excel
import server.scouting.export as export
import server.season.s2019.view.updater as u


class Viewer:
    def __init__(self, alone=True):
        self.alone = alone

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
    def backup(self):
        export.ExportBackup.run_backup(server.model.event.EventDal.get_current_event()[1])
        return 'Success. <a href="/view">Viewer</a>'


    @cherrypy.expose
    def updateAllGraphs(self):
        u.update_graph()

    @cherrypy.expose
    def output(self):
        excel.write_to_excel(excel.rnk_rpt2018a)
        return 'Success. <a href="/view">Viewer</a>'

    @cherrypy.expose
    def restore(self, path):
        self.export.run_restore(path)
        return open(s_config.web_sites("reset.html")).read()

    @cherrypy.expose
    def selectionplan(self):
        return graphing.graph_short_event()
        #return open(s_config.web_data('eventData.html')).read() 

    @cherrypy.expose
    def eventplan(self):
        return graphing.graph_long_event()
        #return open(s_config.web_data('longEventData.html')).read() 

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
        print(out)
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

        return out.replace('{Data}', graphing.examine_match(self.teamsList(setMatch)))

    @cherrypy.expose
    def customplan(self, red1, red2, red3, blue1, blue2, blue3):
        out = open(s_config.web_sites('graphing.html')).read()
        teams = [red1, red2, red3, blue1, blue2, blue3]
        out = out.replace('{Match}', 'Custom')
        out = out.replace('{Schedule}', str(teams))
        out = out.replace('{After}', 'Updated: ' + event.EventDal.get_current_match())

        return out.replace('{Data}', graphing.graph_match(teams)) 


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
    conf = {"/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': s_config.web_base()},
    "/usr/lib/python3.6/site-packages/bokeh/server/static/": {'tools.staticdir.on': True, 'tools.staticdir.dir': s_config.web_scripts("")}}

    cherrypy.tree.mount(Viewer(), '/view', config=conf)
    cherrypy.quickstart(Start(), '/')
