import server.season.s2018.api_measures as s2018api
import server.model.dal as sm_dal
import server.model.setup as sm_setup


def test_colors():
    s2018api.download_platform_color()
    # print(sm_dal.task_ids)
    # sm_setup.load_game_sheet("2018")
