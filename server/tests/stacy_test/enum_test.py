import server.model.match as smm

def test_enum():
    smm.MatchDal.insert_match_task('5468', 'startItem', '007-q',
                                              'auto', 'Cargo', 0, 0, 0)