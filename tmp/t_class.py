# https://data.eastmoney.com/stockdata/000063.html

from scripts_stock.parse_download_data.fuquan_dfcf_parse import parse_fuquan_data
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.utils.process_folder import delete_files_in_folder
from scripts_stock.utils.logging_set import *
from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.datetime.quater_end import *
import wget  # 导入wget库
from scripts_stock.utils.json_to_df import read_txt_file
import pandas as pd
import os
import re
import json
from pathlib import Path
import time
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.datetime.date_function import date_today_yesterday

class DownloadBaseClass():
    def __init__(self):
        self.page_name = 1
        self.tmp_data_txt_name = ''
        self.save_tmp_txt_dir = ''
        self.save_csv_dir = ''
        self.download_url = ''
        self.tmp_csv_name = ''
        self.final_data_name = ''

    def print_data(self):
        print("123")

class DownloadFinReport(DownloadBaseClass):
    def __init__(self):
        self.page_name = 1
        self.tmp_data_txt_name = ''
        self.save_tmp_txt_dir = ProjectDir.download_basic_data_dir
        self.save_csv_dir = ProjectDir.parse_data_basic_dir
        self.download_url = ''
        self.tmp_csv_name = ''
        self.final_data_name = os.path.join(
            self.save_csv_dir, "stock_basic_data.csv")

    def tt(self):
        self.print_data()
        super().print_data()


if __name__ == "__main__":
    aa = DownloadFinReport()
    print(aa.tt())
