import cherrypy

class Scouting(object):
    def __init__(self):
        self.actions = {}
        self.actions['match'] = Match()
        self.actions['event'] = Event()

    def _cp_dispatch(self, vpath):
        action = vpath.pop()
        cherrypy.request.params['vpath'] = vpath
        return self.actions[action]

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name

class Match(object):
    @cherrypy.expose
    def index(self,vpath):
        return 'About match %s...' % (vpath.pop())

class Event(object):
    @cherrypy.expose
    def index(self, vpath):
        return 'About event %s...' % (vpath.pop())

if __name__ == '__main__':
    cherrypy.quickstart(Scouting())