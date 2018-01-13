import json


class Section(object):
    def __init__(self, line):
        value = line.split(',')
        self.actor = value[0]
        self.observer = value[1]
        self.phase = value[2]
        self.category = value[3]
        self.position = value[4]
        self.newpart = value[5].lower()
        self.tasks = value[6].split('|')


class Observers(object):
    def load(self):
        with open("scouting/observertasks.csv", "r") as text:
            out = ''
            for line in text:
                if 'actor,observer' not in line:
                    category = Section(line)
                    data = json.dumps(category, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)
                    out += data + '\n'
            return out
