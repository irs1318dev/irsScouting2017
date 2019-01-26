import server.model.match as smm
import server.scoutingapi as ssa


def test_enum():
    ssa.Scouting.matchteamtask(ssa.Scouting(),'004-q','2915','pickSide','auto')
