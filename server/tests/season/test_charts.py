import os.path
import os

import server.season.s2019.view.sixteam as sixteam
import server.model.event as sme
import server.season.s2019.view.oneteam as oneteam
import server.season.s2019.view.pointschart as pointschart


def test_sixteam():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('030-q')
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          r"..\..\..\..\scouting2019")))
    sixteam.pages_6t('010-q')
