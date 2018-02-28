import pandas

import server.view.dataframes as sv_df
import server.view.excel as sv_xl


# def test_measure_summary_df():
#     df = sv_df.measure_summary_df()
#     assert list(df.columns) == ['team',  'phase', 'task', 'actor', 'matches',
#                                 'sum_successes', 'max_successes',
#                                 'min_successes', 'count_successes',
#                                 'avg_successes', 'sum_attempts', 'max_attempts',
#                                 'min_attempts', 'count_attempts',
#                                 'avg_attempts', 'max_cycle_times',
#                                 'min_cycle_times', 'avg', 'count_cycle_times']
#
#
# def test_excel():
#     sv_xl.convert_to_excel(sv_df.ranking_df(12))