from base64 import b64encode
from urllib import request

import auth


def getSched(event, season, level="qual"):
    # build authorization token
    raw_token = auth.username + ":" + auth.key
    token =  "Basic " + b64encode(raw_token)

    # build url

    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/schedule/" +
           event + "?tournamentLevel=" + level)

    # build headers

    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = request.Request(url, headers=hdrs)

    # send url request
    sched = request.urlopen(req)
    return sched.read()


def getEvents(event, season, tournamentLevel):
    pass


def getMatchResults(event, season, matchNumber, tournamentLevel):
    raw_token = auth.username + ":" + auth.key
    token = "Basic " + b64encode(raw_token)


    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/matches/" +
           event + "?matchNumber=" + matchNumber + "&tournamentLevel=" + tournamentLevel)
    print(url)


    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = request.Request(url, headers=hdrs)

    results = request.urlopen(req)
    return results.read()


def getMatchScores(event, season, tournamentLevel):
    raw_token = auth.username + ":" + auth.key
    token = "Basic " + b64encode(raw_token)


    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/scores/" + event + "/" + tournamentLevel)
    print(url)

    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = request.Request(url, headers=hdrs)

    results = request.urlopen(req)
    return results.read()
