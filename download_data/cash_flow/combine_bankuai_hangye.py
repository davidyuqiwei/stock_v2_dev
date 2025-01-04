import wget  # 导入wget库
import os
from scripts_stock.cfg.set_dir import *
import pandas as pd
import re
from scripts_stock.utils.json_to_df import read_txt_file
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.download_data.cash_flow.colunm_name import col_fields, keep_col  # type: ignore
from scripts_stock.utils.process_folder import delete_files_in_folder
import time
from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.logging_set import *
from scripts_stock.utils.datetime.date_function import date_today_yesterday
from scripts_stock.utils.json_to_df import read_txt_file
import json


class CombineCashData:
    def __init__(self):
        self.save_bankuai_csv_dir = ProjectDir.parse_data_dir_bankuai_cash_flow
        self.save_hangye_csv_dir = ProjectDir.parse_data_dir_hangye_cash_flow

    def combine_data(self):
        df1 = DataFrameProcess.combine_all_dataframe_in_dir(
            self.save_bankuai_csv_dir)
        print(df1.shape)
        #df1.columns = col_fields
        return df1


if __name__ == "__main__":
    aa = CombineCashData().combine_data()
    print(aa)