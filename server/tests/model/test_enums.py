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

def test_percentage(test_event2):
    scouting = ssa.Scouting()

    scouting.matchteamtask('002-q', '3220', 'others', 'finish', '0')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('3220', '002-q')))
    print(enum[0])
    assert enum[0]['task'] == 'others'
    assert enum[0]['cycle_times'] == 0

    scouting.matchteamtask('002-q', '3220', 'others', 'finish', '30')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('3220', '002-q')))
    print(enum[0]['cycle_times'])
    assert enum[0]['task'] == 'others'
    assert enum[0]['cycle_times'] == 30

    scouting.matchteamtask('002-q', '3220', 'others', 'finish', '-10')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('3220', '002-q')))
    print(enum[0]['cycle_times'])
    assert enum[0]['task'] == 'others'
    assert enum[0]['cycle_times'] == 0

    scouting.matchteamtask('002-q', '3220', 'others', 'finish', '110')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('3220', '002-q')))
    print(enum[0]['cycle_times'])
    assert enum[0]['task'] == 'others'
    assert enum[0]['cycle_times'] == 100

    scouting.matchteamtask('002-q', '3220', 'others', 'finish')
    enum = json.loads(svu.jsonify(scouting.matchteamtasks('3220', '002-q')))
    print(enum[0]['cycle_times'])
    assert enum[0]['task'] == 'others'
    assert enum[0]['cycle_times'] == 0




