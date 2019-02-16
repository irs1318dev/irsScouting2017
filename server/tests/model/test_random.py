import server.model.event as sme
import server.model.random_data

# def test_stuff():
#     sm_random_data.add_poisson_measures("test_holoviews", "1318", "placeScale",
#                                         "auto", 4, 0.1, 0.7, sql_output=True)


def test_add_event():
    server.model.random_data.create_event("waiss", "1318", "wayak", "2018")
    sme.EventDal.set_current_event('turing', '2017')
    sme.EventDal.delete_event('waiss', '1318')

