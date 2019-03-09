import server.season.s2019.view.updater as u
import server.config as sc
import time
import datetime
import os


def test_updater():
    c = datetime.datetime.now().strftime('%D %H:%M')
    u.update_graph()
    a = time.localtime(os.path.getmtime(sc.output_path('2019') + '\\rankingtable.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path('2019') + '\\oneteam_index.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path('2019') + '\\index.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
    a = time.localtime(os.path.getmtime(sc.output_path('2019') + '\\pointschart.html'))
    b = time.strftime("%D %H:%M", a)
    assert c <= b
