import time
import datetime
import os

import server.season.s2019.view.updater as u
import server.config as sc
import server.model.event as sme


def test_updater():
    sme.EventDal.set_current_event('wayak', '2019')
    sme.EventDal.set_current_match('060-q')
    c = datetime.datetime.now().strftime('%D %H:%M')
    u.update_graph()
    a = time.localtime(os.path.getmtime(sc.output_path() + '\\rankingtable.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path() + '\\oneteam_index.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path() + '\\index.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path() + '\\pointschart.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
