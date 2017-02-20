class TabletDAL(object):
    def __init__(self, position, page):
        self.position = position
        self.page = page

    def write(self):
        s = self.position + ":" + self.page + ' '
        return s
