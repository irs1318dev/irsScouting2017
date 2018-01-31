"""Tests every method in server.config.py
"""
import server.config


def test_web_sites():
    assert server.config.web_sites("admin.html") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                    r'\irsScouting2017\server\web\sites\admin.html'
    assert server.config.web_sites("directions.html") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                         r'\irsScouting2017\server\web\sites\directions.html'
    assert server.config.web_sites("selection.html") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                         r'\irsScouting2017\server\web\sites\selection.html'


def test_web_scripts():
    assert server.config.web_scripts("selectteam.js") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                         r'\irsScouting2017\server\web\scripts\selectteam.js'
    assert server.config.web_scripts("showteam.js") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                       r'\irsScouting2017\server\web\scripts\showteam.js'
    assert server.config.web_scripts("styles.css") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                      r'\irsScouting2017\server\web\scripts\styles.css'
    assert server.config.web_scripts("tablets.txt") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                       r'\irsScouting2017\server\web\scripts\tablets.txt'


def test_web_data():
    assert server.config.web_data("alliances.csv") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                      r'\irsScouting2017\server\web\data\alliances.csv'
    assert server.config.web_data("climb_chart.html") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                         r'\irsScouting2017\server\web\data\climb_chart.html'
    assert server.config.web_data("turing_2017_0421_1036") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                              r'\irsScouting2017\server\web\data\turing_2017_0421_1036'

def test_web_images():
    assert server.config.web_images("Climbing.png") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                       r'\irsScouting2017\server\web\images\Climbing.png'
    assert server.config.web_images("Gears.png") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                    r'\irsScouting2017\server\web\images\Gears.png'

def test_scouting():
    assert server.config.scouting("alliance.py") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                    r'\irsScouting2017\server\scouting\alliance.py'
    assert server.config.scouting("event.py") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                 r'\irsScouting2017\server\scouting\event.py'
    assert server.config.scouting("observertasks.csv") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                          r'\irsScouting2017\server\scouting\observertasks.csv'


def test_TestJson():
    assert server.config.TestJson("pnw_events.json") == r'C:\Users\IRS\OneDrive\Projects\scouting2017' \
                                                        r'\irsScouting2017\server\TestJson\pnw_events.json'

