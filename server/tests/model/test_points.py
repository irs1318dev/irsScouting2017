import pandas as pd
import server.view.util as svu
import server.season.s2019.view.points as sssvp
import numpy as n


def test_points():
    d = {'hatch': [1, 2, 3], 'cargo': [2, 0, 4], 'climb1': [1, 0, 1], 'climb2': [1, 0, 3], 'climb3': [1, 2, 3]}
    df = pd.DataFrame(data=d, index=[0, 1, 2])
    a = svu.to_points(df['hatch'], sssvp.points['setTotalHatches'])
    b = svu.to_points(df['cargo'], sssvp.points['setTotalCargos'])
    c = svu.to_points(df['climb1'], sssvp.points['setTotalClimb1'])
    e = svu.to_points(df['climb2'], sssvp.points['setTotalClimb2'])
    f = svu.to_points(df['climb3'], sssvp.points['setTotalClimb3'])
    assert a.at[0] == 2
    assert a.at[1] == 4
    assert b.at[0] == 6
    assert b.at[2] == 12
    assert c.at[0] == 3
    assert c.at[1] == 0
    assert e.at[0] == 6
    assert e.at[2] == 18
    assert f.at[0] == 12
    assert f.at[2] == 36

