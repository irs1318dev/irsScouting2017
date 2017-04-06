import scouting.match
import os.path


class Alliance:
    def __init__(self, number):
        self.number = number
        self.teams = ['0', '0', '0']

    def write(self):
        out = ''
        i = 1
        for team in self.teams:
            out += str(self.number) + ',' + team + ',' + str(i) + '\n'
            i += 1
        return out

    def read(self, line):
        data = line.split(',')
        self.teams[int(data[2]) - 1] = data[1]


class AllianceSet:
    alliances = list({Alliance(1)})
    teams = []
    unset = []
    last = ''

    def __init__(self):
        self.matchDal = scouting.match.MatchDal
        i = 1
        while i < 8:
            i += 1
            self.alliances.append(Alliance(i))
        self.currenta = 0
        self.currenti = 0
        self.csv = ''

    def start(self):
        self.teams = self.matchDal.pitteams().split('[')[1].replace(']}', '').split(',')
        self.unset = self.teams

        if os.path.exists("web/data/alliances.csv"):
            self.csv = open("web/data/alliances.csv")
            for line in self.csv:
                if 'na' not in line and 'All' not in line:
                    self.alliances[int(line.split(',')[0]) - 1].read(line)
            self.csv.close()

    def set(self, team):
        if self.currenta > -1:
            self.alliances[self.currenta].teams[self.currenti] = team
            self.unset.remove('"' + team + '"')

        if self.currenti < 2:
            self.currenta += 1
            if self.currenta > 7:
                self.currenti += 1
                if self.currenti == 1:
                    self.currenta = 0
                else:
                    self.currenta = 7
        else:
            self.currenta -= 1

        if team == self.last.replace('"', ''):
            self.last = ''

    def choose(self, index):
        index = int(index)

        self.currenta = int(index / 8)
        self.currenti = int(index % 8)

        if self.alliances[self.currenta].teams[self.currenti] != '0':
            self.last = '"' + self.alliances[self.currenta].teams[self.currenti] + '"'
            self.unset.append(self.last)
            self.alliances[self.currenta].teams[self.currenti] = '0'

    def output(self):
        self.csv = open('web/data/alliances.csv', 'w')
        self.csv.write('Alliance, Team, Station\n')
        for alliance in self.alliances:
            self.csv.write(alliance.write())
        for team in self.unset:
            self.csv.write('na,' + team + ',na\n')
        self.csv.close()


class AlliancePage:
    alliances = AllianceSet()

    def __init__(self):
        self.set = False

    def start(self):
        if not self.set:
            self.alliances.start()
            self.set = True

    def unset(self):
        out = ''
        if self.alliances.last != '':
            out = '<input type="submit" value={Team} onclick="set({Team1});"/><br>'
            out = out.replace('{Team}', self.alliances.last)
            out = out.replace('{Team1}', self.alliances.last.replace('"', "'"))

        i = 0
        l = 1
        self.alliances.unset.sort()
        while l < 7:
            for team in self.alliances.unset:
                if len(team) == l:
                    i += 1
                    out += '<input type="submit" value={Team} onclick="set({Team1});"/>'
                    out = out.replace('{Team}', team)
                    out = out.replace('{Team1}', team.replace('"', "'"))

                    if i % 3 == 0:
                        out += '<br>'
            l += 1
        return out

    def shift(self, a):
        a = int(a)
        while a < 8:
            self.alliances.alliances[a].number -= 1
            self.alliances.alliances[a - 1] = self.alliances.alliances[a]
            a += 1
        self.alliances.alliances[7] = Alliance(8)

    def selections(self, page):
        a = 0
        end = False
        for alliance in self.alliances.alliances:
            out = ''
            i = 0
            empty = True
            while i < 3:
                team = alliance.teams[i]
                if team != '0':
                    empty = False

                out += '<input type="submit" value="{Team}" onclick="choose({index});"/><br>'
                out = out.replace('{index}', "'" + str(a * 8 + i) + "'")

                if a == self.alliances.currenta and i == self.alliances.currenti:
                    out = out.replace('{Team}', '--' + team + '--')
                else:
                    out = out.replace('{Team}', team)

                i += 1
            if empty:
                end = True
            else:
                if end:
                    out += '<a href="/view/selection?shift={a}"><--</a>'
                    out = out.replace('{a}', str(a))
                    end = False
            a += 1

            page = page.replace('{Alliance' + str(alliance.number) + '}', out)
        return page
