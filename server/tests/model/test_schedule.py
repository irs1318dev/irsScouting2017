import server.model.schedule as sc
import server.config as cfg
import sqlalchemy as a
import server.model.connection as c


def test_manual_Entry():
    sc.manual_Entry(cfg.tests_model_test_data("manual_Entry_test.csv"))
    select = a.text("SELECT team FROM schedules WHERE match = '999' AND team = '1742';")
    conn = c.engine.connect()
    b = conn.execute(select).scalar()
    assert b == '1742'
    select = a.text("DELETE FROM schedules WHERE match = '990'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '991'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '992'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '993'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '994'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '995'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '996'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '997'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '998'")
    conn.execute(select)
    select = a.text("DELETE FROM schedules WHERE match = '999'")
    conn.execute(select)
    conn.close()