import datetime
import os.path
import string

import pandas as pd
import xlsxwriter

import server.config as s_config
import server.model.event as sm_event
import server.view.dataframes as sv_dataframes


def convert_to_excel(dataframe, event=None, season=None):
    if event is None and season is None:
        _, event, season = sm_event.EventDal.get_current_event()

    file_name = (event + "_" + season + "_" +
                 datetime.datetime.now().strftime("%Y%b%d_%H%M%S") +
                 ".xlsx")
    path_name = s_config.web_data(file_name)
    writer = pd.ExcelWriter(path_name, engine='xlsxwriter')
    dataframe.to_excel(writer, "All", startrow=4, merge_cells=False)

    phase_row = 2
    actor_row = 3
    task_row = 4
    stat_row = 5

    label_row = 4
    col_idx = 1
    return path_name


def write_to_excel(num_matches=12, event=None, season=None):
    if event is None and season is None:
        _, event, season = sm_event.EventDal.get_current_event()
    file_name = (event + "_" + season + "_" +
                 datetime.datetime.now().strftime("%Y%b%d_%H%M%S") +
                 ".xlsx")
    path_name = s_config.web_data(file_name)
    df_rnk = sv_dataframes.ranking_df(num_matches)
    df_matches = sv_dataframes.match_num_df(num_matches)
    wbook = xlsxwriter.Workbook(path_name)

    wsheet1 = wbook.add_worksheet("Rankings")
    stat_row = 5

    header_fmt = wbook.add_format({'bold': True})
    percent_fmt = wbook.add_format({'num_format': "0%"})
    num_fmt = wbook.add_format({'num_format': "0.0"})

    wsheet1.write_string(stat_row, 0, "team", header_fmt)
    teams = [int(team_num) for team_num in df_rnk.index.values]
    wsheet1.write_column("A7", teams, header_fmt)

    wsheet1.write_string(stat_row, 1, "matches", header_fmt)
    wsheet1.write_column("B7", list(df_matches["matches"]))

    def _xl_colname(idx):
        # Converts integer column index to Excel column address.
        # i.e., idx=0 -> A, idx=25 -> Z, idx=26 -> AA, etc.
        if idx < 0 or idx >= 702:
            raise IndexError("Index value must be integer between 0 and 702.")
        letters = list(string.ascii_uppercase)
        idx_1, idx_2 = divmod(idx, 26)
        if idx_1 ==0:
            return letters[idx_2]
        else:
            return letters[idx_1 - 1] + letters[idx_2]

    # col_def keys:
    #   "phase", "actor", "task", "stat", "format", "task_label", "stat_label"


    def _write_col(col_idx, phase, actor, task, stat, data_format,
                  task_label=None, stat_label=None):

        headers = [phase, actor, task if task_label is None else task_label,
                   stat if stat_label is None else stat_label]
        try:
            data = [_nan_to_zero(x) for x
                    in df_rnk[phase][actor][task][stat]]
        except KeyError:
            print("ERROR: ", phase, actor, task, stat)
            return col_idx
        wsheet1.write_column(_xl_colname(col_idx) + "3", headers, header_fmt)
        wsheet1.write_column(_xl_colname(col_idx) + "7", data, data_format)

        return col_idx + 1

    def _write_col2(col_idx, col_def):
        phase = col_def["phase"]
        if phase is None:
            # Add Blank Column
            return col_idx + 1

        actor = col_def["actor"]
        task = col_def["task"]
        stat = col_def["stat"]

        task_label = (None if "task_label" not in col_def
                      else col_def["task_label"])
        stat_label = (None if "stat_label" not in col_def
                      else col_def["stat_label"])
        if "col_format" in col_def and col_def["col_format"] == "percent":
            col_format = percent_fmt
        else:
            col_format = num_fmt

        headers = [phase, actor, task if task_label is None else task_label,
                   stat if stat_label is None else stat_label]
        try:
            data = [_nan_to_zero(x) for x
                    in df_rnk[phase][actor][task][stat]]
        except KeyError:
            print("ERROR: ", phase, actor, task, stat)
            return col_idx
        wsheet1.write_column(_xl_colname(col_idx) + "3", headers, header_fmt)
        wsheet1.write_column(_xl_colname(col_idx) + "7", data, col_format)

        return col_idx + 1

    cols = [{"phase": "auto", "actor": "robot", "task": "autoLine",
             "stat": "avg_successes", "stat_label": "average",
             "col_format": "percent"},
            {"phase": "auto", "actor": "robot", "task": "placeSwitch",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "placeSwitch",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "placeScale",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "placeExchange",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "placeOpponent",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": None},
            {"phase": "teleop", "actor": "robot", "task": "placeSwitch",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "finish", "actor": "robot", "task": "parkPlatform",
             "stat": "avg_successes", "stat_label": "average",
             "col_format": "percent"},
            {"phase": "finish", "actor": "robot", "task": "makeClimb",
             "stat": "avg_successes", "stat_label": "average",
             "col_format": "percent"},
            {"phase": "teleop", "actor": "robot", "task": "defendRobot",
             "stat": "avg_attempts", "stat_label": "avg_attempts"},
            {"phase": "teleop", "actor": "robot", "task": "defendRobot",
             "stat": "avg_successes", "stat_label": "avg_successes"},
            {"phase": None},
            {"phase": "finish", "actor": "robot", "task": "disabled",
             "stat": "avg_attempts", "stat_label": "temp_avg"},
            {"phase": "finish", "actor": "robot", "task": "disabled",
             "stat": "avg_successes", "stat_label": "perm_avg"},
            {"phase": "finish", "actor": "team", "task": "getFoul",
             "stat": "avg_attempts", "stat_label": "avg_attempt"},
            {"phase": None},
            {"phase": "teleop", "actor": "robot", "task": "pickupFloor",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "pickupExchange",
             "stat": "avg_successes", "stat_label": "average"},
            {"phase": "teleop", "actor": "robot", "task": "pickupCubeZone",
             "stat": "avg_successes", "stat_label": "average"}
            ]

    col_idx = 2

    for col in cols:
        col_idx = _write_col2(col_idx, col)
    wbook.close()


def _nan_to_zero(elmt):
    return 0 if pd.isnull(elmt) else elmt








def get_report(name):
    name = os.path.abspath(name)

    tasks = ['placeGear', 'shootHighBoiler', 'shootLowBoiler', 'pushTouchPad',
             'climbRope', 'defendMovement', 'moveBaseline']
    raw_df = get_rankings(None, tasks)
    final_df = pd.DataFrame()
    final_df['AutoGearMatch'] = raw_df['auto']['robot']['placeGear']['matches']
    #final_df['AutoGearAttp'] = raw_df['auto']['robot']['placeGear']['sum_attempts']
    final_df['pGearAutoAvg'] = raw_df['auto']['robot']['placeGear']['sum_successes'] / raw_df['auto']['robot']['placeGear']['matches']
    final_df['pGearAuto%'] = raw_df['auto']['robot']['placeGear']['sum_successes'] / raw_df['auto']['robot']['placeGear']['sum_attempts']

    final_df['pGearTeleAvg'] = raw_df['teleop']['robot']['placeGear']['sum_successes'] / raw_df['teleop']['robot']['placeGear']['matches']
    final_df['pGearTele%'] = raw_df['teleop']['robot']['placeGear']['sum_successes'] / raw_df['teleop']['robot']['placeGear']['sum_attempts']

    final_df['HighBoilerAutoAvg'] = raw_df['auto']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['matches']
    final_df['HighBoilerTeleAvg'] = raw_df['teleop']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['matches']

    final_df['pushTouchPad'] = raw_df['finish']['robot']['pushTouchPad']['sum_successes'] / raw_df['finish']['robot']['pushTouchPad']['matches']
    #final_df['climbRope'] = raw_df['finish']['robot']['climbRope']['sum_successes'] / raw_df['finish']['robot']['climbRope']['matches']
    final_df['defendMovement'] = raw_df['teleop']['robot']['defendMovement']['sum_successes'] / raw_df['teleop']['robot']['defendMovement']['matches']
    final_df['moveBaseline'] = raw_df['auto']['robot']['moveBaseline']['sum_successes'] / raw_df['auto']['robot']['moveBaseline']['matches']

    final_df['HighBoilerAuto%'] = raw_df['auto']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['sum_attempts']
    final_df['HighBoilerTele%'] = raw_df['teleop']['robot']['shootHighBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootHighBoiler']['sum_attempts']

    final_df['LowBoilerAuto%'] = raw_df['auto']['robot']['shootLowBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootLowBoiler']['sum_attempts']
    final_df['LowBoilerTele%'] = raw_df['teleop']['robot']['shootLowBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootLowBoiler']['sum_attempts']

    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    final_df.to_excel(writer, sheet_name="All")

    # Format workbook

    wkbk = writer.book
    wksheet = writer.sheets['All']

    width = 8

    dec_format = wkbk.add_format({'num_format': '0.00'})

    #dec_format_grey = wkbk.add_format({'num_format': '0.0'})
    #dec_format_grey.set_bg_color('#D3D3D3')

    per_format = wkbk.add_format({'num_format': '0%'})

    #per_format_grey = wkbk.add_format({'num_format': '0%'})
    #per_format_grey.set_bg_color('#D3D3D3')

    int_format_grey = wkbk.add_format({'num_format': '0'})

    # wksheet.set_column('B1:B1', width, text_60)
    # wksheet.set_column('C1:C1', width, text_60)
    format = wkbk.add_format()
    format.set_rotation(70)

    name = ['AutoGearMatch','pGearAutoAvg','pGearAuto%','pGearTeleAvg','pGearTele%','HighBoilerAutoAvg',
            'HighBoilerTeleAvg','pushTouchPad','defendMovement','moveBaseline','HighBoilerAuto%','HighBoilerTele%',
             'LowBoilerAuto%','LowBoilerTele%']
    val = 1
    for i in name:
        wksheet.write(0, val,i, format)
        val = val + 1
    wksheet.set_column('B2:B100', width, int_format_grey)
    wksheet.set_column('C:C', width, dec_format)
    wksheet.set_column('D:D', width, per_format)
    wksheet.set_column('E:E', width, dec_format)
    wksheet.set_column('F:F', width, per_format)
    wksheet.set_column('G:G', width, dec_format)
    wksheet.set_column('H:H', width, dec_format)
    wksheet.set_column('I:I', width, dec_format)
    wksheet.set_column('J:J', width, dec_format)
    wksheet.set_column('K:K', width, dec_format)
    wksheet.set_column('L:L', width, per_format)
    wksheet.set_column('M:M', width, per_format)
    wksheet.set_column('N:N', width, per_format)
    wksheet.set_column('O:O', width, per_format)

    # for row in range(0, 100):
    #     if (row % 2 == 1):
    #         wksheet['C' + str(row)].style.number_format.format_code = '0.0'
    #
    #         # wksheet.set_cell(row, 'B', width, int_format_grey)
    #         # wksheet.set_cell(row, 'C', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'D', width, per_format_grey)
    #         # wksheet.set_cell(row, 'E', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'F', width, per_format_grey)
    #         # wksheet.set_cell(row, 'G', width, per_format_grey)
    #         # wksheet.set_cell(row, 'H', width, per_format_grey)
    #         # wksheet.set_cell(row, 'I', width, per_format_grey)
    #         # wksheet.set_cell(row, 'J', width, per_format_grey)
    #         # wksheet.set_cell(row, 'K', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'L', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'M', width, dec_format_grey)
    #     else:
    #         pass
    #         # wksheet.set_cell(row, 'B', width, None)
    #         # wksheet.set_cell(row, 'C', width, dec_format)
    #         # wksheet.set_cell(row, 'D', width, per_format)
    #         # wksheet.set_cell(row, 'E', width, dec_format)
    #         # wksheet.set_cell(row, 'F', width, per_format)
    #         # wksheet.set_cell(row, 'G', width, per_format)
    #         # wksheet.set_cell(row, 'H', width, per_format)
    #         # wksheet.set_cell(row, 'I', width, per_format)
    #         # wksheet.set_cell(row, 'J', width, per_format)
    #         # wksheet.set_cell(row, 'K', width, dec_format)
    #         # wksheet.set_cell(row, 'L', width, dec_format)
    #         # wksheet.set_cell(row, 'M', width, dec_format)

    writer.save()

