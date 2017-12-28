from base64 import b64encode
from urllib.request import Request, urlopen

import Server.auth


def getSched(event, season, level="qual"):
    # build authorization token
    raw_token = Server.auth.username + ":" + Server.auth.key
    token =  "Basic " + b64encode(raw_token)

    # build url

    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/schedule/" +
           event + "?tournamentLevel=" + level)

    # build headers

    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = Request(url, headers=hdrs)

    # send url request
    sched = urlopen(req)
    return sched.read()


#TODO: Get rid of empty function
def getEvents(event, season, tournamentLevel):
    pass


def getMatchResults(event, season, matchNumber, tournamentLevel):
    raw_token = Server.auth.username + ":" + Server.auth.key
    token = "Basic " + b64encode(raw_token)


    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/matches/" +
           event + "?matchNumber=" + matchNumber + "&tournamentLevel=" + tournamentLevel)
    print(url)


    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = Request(url, headers=hdrs)

    results = urlopen(req)
    return results.read()


def getMatchScores(event, season, tournamentLevel):
    raw_token = Server.auth.username + ":" + auth.key
    token = "Basic " + b64encode(raw_token)


    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/scores/" + event + "/" + tournamentLevel)
    print(url)

    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = Request(url, headers=hdrs)

    results = urlopen(req)
    return results.read()
