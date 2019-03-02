import pytest
import server.scouting.tablet as tablet


def test_constructor():
"""tests the gettablets with the initial setup
"""
    tablets = tablet.TabletList()
    result = tablets.gettablets()
    assert result == 'TestSystem:Waiting    <br>   '


def test_insertTablets():
"""testing function inserttablets from tablet.py
"""
    tablets = tablet.TabletList()
    result = tablets.inserttablets("{TestSystem}")
    assert result == "Waiting"


def test_settablet():
"""testing that duplicate tablets aren;t added to the tablet list
"""
    tablets = tablet.TabletList()
    newTablet = tablet.Tablet("testOne", "Auto", 1)
    result = tablets.settablet(newTablet)
    assert result == False
    expectedTablet = tablets.get(1)
    assert expectedTablet.position == "testOne"
    assert expectedTablet.ip == 1
    assert expectedTablet.page == "Auto"
    assert tablets.length() == 2
    result = tablets.settablet(newTablet)
    assert tablets.length() == 2


def test_settable_assignNewPage():
"""testing that the booleans are correct for page
"""
    tablets = tablet.TabletList()
    newTablet = tablet.Tablet("testOne", "Auto", 1)
    result = tablets.settablet(newTablet)
    assert tablets.length() == 2
    newTablet.page = "test"
    result = tablets.settablet(newTablet)
    assert result == False
    newTablet.page == "Auto"
    result = tablets.settablet(newTablet)
    assert tablets.getIndex(0).page == "Waiting"


def test_settablet_nextmatch():
"""testing that if all tablets are set to waiting, the next match can start
"""
    tablets = tablet.TabletList()
    newTablet = tablet.Tablet("testOne","Waiting",1)
    tablets.settablet(newTablet)
    newTablet = tablet.Tablet("testTwo","Waiting", 2)
    tablets.settablet(newTablet)
    assert tablets.getIndex(0).page == "Reset"


def test_findnext():
"""testing method findnext in tablet.py
"""
    tablets = tablet.TabletList()
    newTablet = tablet.Tablet("testTwo", "Waiting","2")
    result = tablets.findnext(newTablet)
    assert result == False
    newTablet.position = "Pit"
    result = tablets.findnext(newTablet)
    assert result == False



