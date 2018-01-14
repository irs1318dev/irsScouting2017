import base64
from urllib.request import Request, urlopen

import server.auth


def _send_http_request(url):
    raw_token = server.auth.username + b":" + server.auth.key
    token = b"Basic " + base64.b64encode(raw_token)
    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = Request(url, headers=hdrs)
    return urlopen(req).read()


def schedule(event, season, level="qual"):
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/schedule/" +
           event + "?tournamentLevel=" + level)
    return _send_http_request(url)


# TODO: Get rid of empty function
def events(event, season, tournamentLevel):
    pass


def match_results(event, season, match_number, level="qual"):
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/matches/" +
           event + "?matchNumber=" + str(match_number) + "&tournamentLevel=" +
           level)
    return _send_http_request(url)


def match_scores(event, season, level="qual"):
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/scores/" +
           event + "/" + level)
    return _send_http_request(url)
