import json
import server.model.match as smm
import server.scoutingapi as ssa
import server.view.util as svu


def test_enum(test_event2):
    scouting = ssa.Scouting()

    # Set enum value
    scouting.matchteamtask('001-q', '4120', 'startPosition', 'auto', 'Center')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('4120', '001-q')))
    assert enum[0]['task'] == 'startPosition'
    assert enum[0]['capability'] == 'Center'

    # Clear enum value
    scouting.matchteamtask('001-q', '4120', 'startPosition', 'auto')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('4120', '001-q')))
    assert enum[0]['task'] == 'startPosition'
    assert enum[0]['capability'] == 0

    # Reset enum value
    scouting.matchteamtask('001-q', '4120', 'startPosition', 'auto', 'Exch')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('4120', '001-q')))
    assert enum[0]['task'] == 'startPosition'
    assert enum[0]['capability'] == 'Exch'

    # Reset enum value
    scouting.matchteamtask('001-q', '4120', 'startPosition', 'auto', 'NonEx')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('4120', '001-q')))
    assert enum[0]['task'] == 'startPosition'
    assert enum[0]['capability'] == 'NonEx'

