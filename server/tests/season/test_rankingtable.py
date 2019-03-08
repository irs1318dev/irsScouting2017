import pathlib

import server.season.s2019.view.rankingtable as rt
import server.model.event as sme


def test_rankingtable():
    # sme.EventDal.set_current_event('test_data', '2019')
    # sme.EventDal.set_current_match('020-q')
    rt.pages_rankingtable()
