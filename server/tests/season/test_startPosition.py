import server.model.event as sm_event
import server.model.match as sm_match


def test_insert_start_position():
    sm_event.EventDal.set_current_event("waiss", "1318")
    sm_match.MatchDal.insert_match_task("4125", "startPosition", "001-q",
                                        "auto", "Exch")
    sm_match.MatchDal.insert_match_task("2148", "startPosition", "001-q",
                                        "auto", "Center")
    sm_match.MatchDal.insert_match_task("6076", "startPosition", "001-q",
                                        "auto", "NonEx")
