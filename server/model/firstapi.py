"""Downloads FRC event data from remote FIRST API server via HTTP.

All FRC event data is stored in a server managed by FIRST and is
available for download via hyptertext transfer protocol (HTTP). The
scouting system downloads match schedules from the FIRST API server
and enters them into the database.

FIRST API documentation, including the required headers, URL format,
and rules for authorization, are available at
http://docs.frcevents2.apiary.io/# .

Module Functions
----------------

`server.model.firstapi.schedule()`: Downloads match schedules.
`server.model.firstapi.match_results()`: Downloads data showing who
won match and high-level match scores.
`server.model.firstapi.match_scores()`: Downloads detailed match result
and scores, including autonomous points, teleop points, fouls, etc.

Authorization
-------------

A username and authorization key is required to use the FIRST API.
Follow the instructions at
https://usfirst.collab.net/sf/projects/first_community_developers/ to
otain a username and authorization key from FIRST. Each team or
individual must have their own authorization key -- no key or username
are provided with the scouting system.

This module assumes the username and authorization key are stored in
server.auth. *They must be stored as **bytes** objects, not as strings.*
This means you must prefix the key or username with a 'b' character.
Example contents of auth module:
```
key = b"authorization key"
usename = b"team_username"
```

**Keep your authorization key private.** Ensure the auth module is listed
in your .gitignore file so it does not inadvertently get posted to
Github. The line `**/auth.py` will cause git to ignore any file named
auth.py, regardless of where it is located.
"""

# todo(stacy) add ability to display event codes.

import base64
import urllib.request

import server.auth


def _send_http_request(url):
    raw_token = server.auth.FIRSTAPI_USER + b":" + server.auth.FIRSTAPI_KEY
    token = b"Basic " + base64.b64encode(raw_token)
    hdrs = {"Accept": "application/json", 'Authorization': token}
    req = urllib.request.Request(url, headers=hdrs)
    return urllib.request.urlopen(req).read()


def schedule(event, season, level="qual"):
    """Download event match schedule from the FIRST API server.

    Args:
        event: (str) A short code that identifies the FRC competition.
        This code is assigned by FIRST. For example, "pncmp" refers to
        the Pacific Northwest district championships.
        season: (str) The four digit year, i.e., "2018", that identifies
        the competition season.
        level: (str) Optional. Either "qual" or "playoff". Defaults to
        "qual".

    Returns: (str) Match schedule formatted as Javascript Object
    Notation (JSON).
    """
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/schedule/" +
           event + "?tournamentLevel=" + level)
    return _send_http_request(url)


def match_results(event, season, match_number, level="qual"):
    """Download high-level match results from the FIRST API server.

    Args:
        event: (str) A short code that identifies the FRC competition.
        This code is assigned by FIRST. For example, "pncmp" refers to
        the Pacific Northwest district championships.
        season: (str) The four digit year, i.e., "2018", that identifies
        the competition season.
        match_number: (str or int): The match number, i.e., 1, 2, 34,
        111, etc.
        level: (str) Optional. Either "qual" or "playoff". Defaults to
        "qual".

    Returns: (str) Match results formatted as Javascript Object
    Notation (JSON).
    """
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/matches/" +
           event + "?matchNumber=" + str(match_number) + "&tournamentLevel=" +
           level)
    return _send_http_request(url)


def match_scores(event, season, level="qual"):
    """Download detailed match scores from the FIRST API server.

    Args:
        event: (str) A short code that identifies the FRC competition.
        This code is assigned by FIRST. For example, "pncmp" refers to
        the Pacific Northwest district championships.
        season: (str) The four digit year, i.e., "2018", that identifies
        the competition season.
        level: (str) Optional. Either "qual" or "playoff". Defaults to
        "qual".

    Returns: (str) Match results formatted as Javascript Object
    Notation (JSON).
    """
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/scores/" +
           event + "/" + level)
    return _send_http_request(url)


def events(season):
    url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/events")
    return _send_http_request(url)


def get_team_names(teamNumber, season='2018'):
        url = ("https://frc-api.firstinspires.org/v2.0/" + season + "/teams?teamNumber=" + teamNumber)
        return _send_http_request(url)
