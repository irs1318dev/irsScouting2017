import cherrypy


class Band(object):
    def __init__(self):
        self.albums = Album()

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['name'] = vpath.pop()
            return self

        if len(vpath) == 3:
            cherrypy.request.params['artist'] = vpath.pop(0)  # /band name/
            vpath.pop(0) # /albums/
            cherrypy.request.params['title'] = vpath.pop(0) # /album title/
            return self.albums

        return vpath

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name

class Album(object):
    @cherrypy.expose
    def index(self, artist, title):
        return 'About %s by %s...' % (title, artist)


if __name__ == '__main__':
    cherrypy.quickstart(Band())
