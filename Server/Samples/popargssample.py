import cherrypy


@cherrypy.popargs('band_name')
class Band(object):
    def __init__(self):
        self.albums = Album()

    @cherrypy.expose
    def index(self, band_name):
        return 'About %s...' % band_name

@cherrypy.popargs('album_title')
class Album(object):
    @cherrypy.expose
    def index(self, band_name, album_title):
        return 'About %s by %s...' % (album_title, band_name)

@cherrypy.popargs('track_num', 'track_title')
class Track(object):
    @cherrypy.expose
    def index(self, band_name, album_title, track_num, track_title):
        return 'About %s ... %s... %s ... %s ... %s' % (album_title, band_name, track_num, track_title)


if __name__ == '__main__':
    cherrypy.quickstart(Band())