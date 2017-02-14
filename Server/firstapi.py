from base64 import b64encode
from urllib2 import Request, urlopen

import auth


def getSched(event, season, level = "qual"):
    # build authorization token
    raw_token = auth.username + ":" + auth.key
    token =  "Basic " + b64encode(raw_token)

    # build url

    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/schedule/" +
           event + "?tournamentLevel=" + level)

    # build headers

    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = Request(url, headers = hdrs)



    # send url request
    sched = urlopen(req)
    return sched.read()

print getSched('WAAMV', '2016', level='qual')

