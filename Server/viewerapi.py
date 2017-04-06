import cherrypy
from cherrypy.lib.static import serve_file
import os.path
import scouting.export
import scouting.output
import scouting.event
import scouting.alliance


class Viewer:
    def __init__(self, alone=True):
        self.alone = alone
        self.export = scouting.export.ExportBackup
        self.alliances = scouting.alliance.AlliancePage()

    @cherrypy.expose
    def index(self):
        out = open('web/sites/view.html').read()
        out = out.replace('{Images}', self.images())

        if self.alone:
            out = out.replace('{Backup}', '<h3><a href="/view/sync">Remote Sync</a></h3>')
            out = out.replace('{Back}', '')
        else:
            out = out.replace('{Backup}', '<h3><a href="/view/backup">Backup Database</a></h3>')
            out = out.replace('{Back}', '<h3><a href="/">Scouting Director</a></h3>')

        return out

    @staticmethod
    def images():
        images = []
        for row in os.walk('web/images'):
            images = str(row).split('[')[2].replace('])', '').split(', ')

        out = ''
        for image in images:
            image = image.replace("'", '')
            out += '<a href="/web/images/' + image + '">' + image.replace('.png', '') + '</a><br>'

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
    def backup(self):
        script = self.export.runBackup(scouting.event.EventDal.get_current_event())
        return '<a href="/view/data?name=' + script + '">Download File</a>'
        # return open("web/resetView.html").read()

    @cherrypy.expose
    def restore(self, path):
        self.export.runRestore(path)
        return open("web/sites/resetView.html").read()

    @cherrypy.expose
    def sync(self):
        return 'WIP'

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

if __name__ == '__main__':
    conf = {
        "/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.quickstart(Viewer(), '/view', config=conf)
