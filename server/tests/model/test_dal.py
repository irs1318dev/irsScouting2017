import server.model.dal as sm_dal


def test_dal():
    sm_dal.rebuild_dicts()

def test_task_options():
    sm_dal.rebuild_dicts()
    print("\n")
    print(sm_dal.task_option_ids.keys())
    print(sm_dal.task_option_ids["startPosition-NonEx"])