
from scripts_stock.parse_download_data.fuquan_dfcf_parse import parse_fuquan_data
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.utils.process_folder import delete_files_in_folder
from scripts_stock.utils.logging_set import *
from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.datetime.quater_end import *
from scripts_stock.data_base.insert_into_db import df_save_to_db

import wget  # 导入wget库
from scripts_stock.utils.json_to_df import read_txt_file
import pandas as pd
import os 
import re
import json
from pathlib import Path
import time

# https://quote.eastmoney.com/zs000300.html#
class DownloadHS300(ProjectDir):
    def __init__(self,ProjectDir):
        self.tmp_data_txt_name = ''
        self.history_days = '3000'
        self.url1 = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery35106073162979112385_1733119474002&secid=1.000300&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt={self.history_days}&_=1733119474029"
        self.save_tmp_txt_dir = ProjectDir.download_data_dir_hs300
        self.save_csv_dir = ProjectDir.parse_data_dir_hs300
        self.tmp_data_txt_name = os.path.join(self.save_tmp_txt_dir, "hs300" + ".txt")
        self.out_df = ''
        self.final_data_name = os.path.join(
            self.save_csv_dir, "hs300.csv")
        
    def download_tmp_txt(self):
        wget.download(self.url1, self.tmp_data_txt_name) 
    
    def parse_hs300_data(self):
        df1 = read_txt_file(self.tmp_data_txt_name)
        dta = re.findall('klines":\\[(.*)]', df1)
        dta1 = dta[0].split("\",")        
        df_list = []

        for k in dta1:
            dta2 = k.replace("\"", "")
            aa = dta2.split(",")
            df_list.append(aa)
        df_out = pd.DataFrame(df_list)
        df_out1 = df_out.iloc[:, 0:7]
        df_out1.columns = ["date", "open", "close","high","low","transaction_volume","transaction_cash"]
        # 解析 JSON 字符串
        df_out1 = df_out1[:-1]
        # self.tmp_csv_name = self.tmp_data_txt_name.replace('.txt','.csv')
        self.out_df = df_out1
        df_out1.to_csv(self.final_data_name, index=False)

    def inser_to_db(self):
        df_save_to_db(self.out_df,target_table="prd_t_hs300_daily")

    def main_run(self):
        try:
            self.download_tmp_txt()
            self.parse_hs300_data()
            #self.inser_to_db()
            delete_files_in_folder(ProjectDir.download_data_dir_hs300)
        except Exception as e:
            TNLog().error("======== download hs300 error =======")
            TNLog().error(e)
            pass
        TNLog().info("==== +++++  finish all download hs300 error  ++++++ =====")


if __name__ == "__main__":
    DownloadHS300(ProjectDir).main_run()