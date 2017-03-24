import threading
from datetime import datetime


class TabletDAL(object):
    def __init__(self, position, page, ip):
        self.position = position
        self.page = page
        self.last = datetime.now().second
        self.ip = ip

    def write(self):
        s = self.position + ":" + self.page
        if self.ip > -1:
            s += ":" + str(self.ip)
        s += "    <br>   "
        return s

    def checkfail(self):
        time = datetime.now().second
        if time - self.last > 20:
            self.page = "Off"


class TabletList(object):
    alltablets = list({TabletDAL('TestSystem', 'Waiting', -1)})

    def settablet(self, newtablet):
        nextmatch = True
        found = False
        i = 0

        while i < len(self.alltablets):
            if self.alltablets[i].position in newtablet.position:
                self.alltablets[i].page = newtablet.page
                if newtablet.ip > -1:
                    self.alltablets[i].ip = newtablet.ip

                found = True
            if self.findnext(self.alltablets[i]):
                nextmatch = False
            i += 1

        if not found:
            self.alltablets.append(newtablet)
            if self.findnext(newtablet):
                nextmatch = False

        if nextmatch and newtablet.position == "Pit":
            nextmatch = False

        if nextmatch:
            self.alltablets[0].page = "Reset"
        if not nextmatch and newtablet.position == "Auto":
            self.alltablets[0].page = "Waiting"

        return nextmatch

    def gettablets(self):
        s = ""

        for tab in self.alltablets:
            s += tab.write()

        return s

    def inserttablets(self, table):
        for tablet in self.alltablets:
            key = '{' + tablet.position + '}'
            table = table.replace(key, tablet.page)

        return table

    @staticmethod
    def findnext(tablet):
        tablet.last = datetime.now().second
        threading.Timer(21, tablet.checkfail).start()

        if "Waiting" in tablet.page:
            return False
        if "Pit" in tablet.position:
            return False
        if "Off" in tablet.page:
            return False
        return True
