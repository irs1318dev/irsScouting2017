import server.model.dal as sm_dal


def test_dal():
    sm_dal.rebuild_dicts()


def test_task_options():
    sm_dal.rebuild_dicts()
    task_option = "startPosition-NonEx"
    option_id = sm_dal.task_option_ids[task_option]
    assert isinstance(option_id, int)
    assert sm_dal.task_option_names[option_id] == task_option
    assert sm_dal.task_option_options[option_id] == "NonEx"