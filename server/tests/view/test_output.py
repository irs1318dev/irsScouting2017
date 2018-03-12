import pandas

import server.view.dataframes as sv_df
import server.view.excel as sv_xl


# def test_measure_summary_df():
#     df = sv_df.measure_summary_df()
#     print(df)
#     # assert set(df.columns) == set(['team',  'phase', 'task', 'actor', 'matches',
#     #                             'sum_successes', 'max_successes',
#     #                             'min_successes', 'count_successes',
#     #                             'avg_successes', 'sum_attempts', 'max_attempts',
#     #                             'min_attempts', 'count_attempts',
#     #                             'avg_attempts', 'max_cycle_times',
#     #                             'min_cycle_times', 'avg', 'count_cycle_times'])
#
#
# def test_ranking_df():
#     df = sv_df.ranking_df(12)
#     print(df)
#
#
# def test_excel1():
#     sv_xl.write_to_excel(12, "week0", "2018")
#
#
# def test_excel2():
#     sv_xl.write_to_excel(sv_xl.rnk_rpt2018a, 12, "wamou", "2018")
#
#
# def test_matches():
#     print(sv_df.match_num_df())