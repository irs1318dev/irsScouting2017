class TabletDAL(object):
    def __init__(self, position, page):
        self.position = position
        self.page = page

    def write(self):
        s = self.position + ":" + self.page + ', '
        return s


class TabletList(object):
    alltablets = list({TabletDAL('TestSystem', 'Waiting')})

    def settablet(self, newtablet):
        nextmatch = True
        found = False
        i = 0

        while i < len(self.alltablets):
            if self.alltablets[i].position in newtablet.position:
                self.alltablets[i].page = newtablet.page
                found = True
            if 'Waiting' not in self.alltablets[i].page and 'Pit' not in newtablet.page:
                nextmatch = False
            i += 1

        if not found:
            self.alltablets.append(newtablet)
            if 'Waiting' not in newtablet.page and 'Pit' not in newtablet.page:
                nextmatch = False

        if nextmatch:
            self.alltablets[0].page = "Reset"
        else:
            self.alltablets[0].page = "Waiting"

        return nextmatch

    def gettablets(self):
        s = ""

        for tab in self.alltablets:
            s += tab.write()

        return s

    def inserttablets(self, table):
        for tablet in self.alltablets:
            table.replace('{' + tablet.position + '}', tablet.page)

        return table
