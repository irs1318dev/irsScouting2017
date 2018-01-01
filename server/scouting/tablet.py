import socket
import psutil


class TabletDAL(object):
    def __init__(self, position, page, ip):
        self.position = position
        self.page = page
        self.ip = ip

    def write(self):
        s = self.position + ":" + self.page
        if self.ip > -1:
            s += ":" + str(self.ip)
        s += "    <br>   "
        return s


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
        if newtablet.page == "Auto":
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
        if "Waiting" in tablet.page:
            return False
        if "Pit" in tablet.position:
            return False
        return True

    def setaddress(self):
        def get_ip_addresses(family):
            for interface, snics in psutil.net_if_addrs().items():
                for snic in snics:
                    if snic.family == family:
                        yield (interface, snic.address)

        ipv4s = list(get_ip_addresses(socket.AF_INET))
        unlinked = list()

        for ip in ipv4s:
            linked = False
            for tablet in self.alltablets:
                if ip is tablet.ip:
                    linked = True
            if not linked:
                unlinked.append(ip)

        return unlinked
