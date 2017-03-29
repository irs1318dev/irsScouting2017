import scouting.match


class Alliance:
    def __init__(self, number):
        self.number = number
        self.teams = []

    def push(self, team):
        i = 0
        while self.teams[i] != '':
            i += 1
        self.teams[i] = team


class AllianceSet:
    def __init__(self):
        self.matchDal = scouting.match.MatchDal
        self.teams = self.matchDal.pitteams().split('[')[1].replace(']}', '').split(',')
        self.alliances = list({Alliance(1)})
        i = 1
        while i < 8:
            i += 1
            self.alliances.append(Alliance(i))
        self.unset = self.teams
        self.current = 0

    def set(self, team):
        self.alliances[self.current].push(team)
        self.unset.remove(team)

    def choose(self, alliance, i=0):
        self.current = alliance
        if self.alliances[alliance].teams[i] != '':
            self.unset.append(self.alliances[alliance].teams[i])
            self.alliances[alliance].teams[i] = ''
