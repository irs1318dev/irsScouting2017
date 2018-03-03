import datetime
import os.path

import pandas as pd

import server.config as s_config
import server.model.event as sm_event
import server.view.dataframes as svd


def convert_to_excel(dataframe):
    event = sm_event.EventDal.get_current_event()
    file_name = (event[1] + "_" + event[2] + "_" +
                 datetime.datetime.now().strftime("%Y%b%d_%H%M%S") +
                 ".xlsx")
    path_name = s_config.web_data(file_name)
    writer = pd.ExcelWriter(path_name, engine='xlsxwriter')
    dataframe.to_excel(writer, "All", merge_cells=False)

    return path_name


def get_Basic_Ranking(name):
    return get_rankings(name, ['moveBaseline', 'placeGear', 'shootHighBoiler', 'shootLowBoiler'])


def get_Path(start):
    ts = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
    excel = start + '_' + event.EventDal.get_current_event()[1] + ts + '.xlsx'
    return 'web/data/' + excel


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

