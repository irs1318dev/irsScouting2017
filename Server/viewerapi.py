import cherrypy
from cherrypy.lib.static import serve_file
import os
import scouting.export
import scouting.output
import scouting.event


class Viewer:
    def __init__(self, alone=True):
        self.alone = alone
        self.export = scouting.export.ExportBackup

    @cherrypy.expose
    def index(self):
        out = open('web/view.html').read()
        out = out.replace('{Images}', self.images())

        if self.alone:
            out = out.replace('{Backup}', '<h3><a href="/view/sync">Remote Sync</a></h3>')
            out = out.replace('{Back}', '')
        else:
            out = out.replace('{Backup}', '<h3><a href="/view/backup">Backup Database</a></h3>')
            out = out.replace('{Back}', '<h5><a href="/">Scouting Director</a></h5>')

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
        return serve_file(os.path.abspath('web/data/' + name), "application/x-download", "attachment")

    @cherrypy.expose
    def output(self):
        excel = scouting.output.get_Path('Report')
        scouting.output.get_report(excel)
        return serve_file(excel, "application/x-download", "attachment")
        # return open("web/resetView.html").read()

    @cherrypy.expose
    def backup(self):
        return self.export.runBackup(scouting.event.EventDal.get_current_event())
        # return open("web/resetView.html").read()

    @cherrypy.expose
    def restore(self, path):
        self.export.runRestore(path)
        return open("web/resetView.html").read()

    @cherrypy.expose
    def sync(self):
        return 'WIP'

if __name__ == '__main__':
    conf = {
        "/web": {'tools.staticdir.on': True, 'tools.staticdir.dir': os.path.abspath('web')}}

    cherrypy.quickstart(Viewer(), '/view', config=conf)
