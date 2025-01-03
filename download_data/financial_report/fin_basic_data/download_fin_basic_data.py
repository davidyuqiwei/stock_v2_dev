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



class DownloadFinReport(ProjectDir):
    def __init__(self, ProjectDir):
        self.page_name = 1
        self.tmp_data_txt_name = ''
        self.save_tmp_txt_dir = ProjectDir.download_basic_data_dir
        self.save_csv_dir = ProjectDir.parse_data_basic_dir
        self.download_url = ''
        self.tmp_csv_name = ''
        self.final_data_name = os.path.join(
            self.save_csv_dir, "stock_basic_data.csv")

    def get_stock_index(self):
        sql_str = f"""
            select distinct SECURITY_CODE as stock_index from r_t_fin_report 
            where substr(REPORTDATE,1,10)='2024-09-30'
        """
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(sql_str, conn)
        return df1["stock_index"].tolist()

    def download_tmp_txt(self):
        today_date, _, _ = date_today_yesterday(150)
        stock_index_list = self.get_stock_index()
        for stock_in in stock_index_list:
            stock_in = str(stock_in).zfill(6)
            try:
                save_name = os.path.join(
                    self.save_tmp_txt_dir, stock_in + "_"+today_date + ".txt")
                self.tmp_data_txt_name = save_name
                url1 = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112301347211140819402_1735200937488&reportName=RPT_STOCK_INDUSTRY_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE%3D%22{stock_in}%22)&_=1735200937489"
                wget.download(url1, save_name)
                time.sleep(5)
                self.parse_basic_data()
            except Exception as e:
                print(e)
                pass
        # file_size_bytes = Path(save_name).stat().st_size
        # # 转换为KB
        # file_size_kb = file_size_bytes / 1024
        return ""

    def parse_basic_data(self):
        df1 = read_txt_file(self.tmp_data_txt_name)
        dta = re.findall('data":\\[(.*)]', df1)
        dta1 = dta[0]
        # 解析 JSON 字符串
        data_dicts = json.loads(dta1)
        # print(data_dicts)
        df = pd.DataFrame([data_dicts])
        # print(df)
        self.tmp_csv_name = self.tmp_data_txt_name.replace('.txt', '.csv')
        df.to_csv(self.tmp_csv_name, index=False)
        return ""

    def combine_basic_data(self):
        df2 = DataFrameProcess.combine_all_dataframe_in_dir(
            self.save_tmp_txt_dir)
        df2.to_csv(self.final_data_name, index=False)

    def main_run(self):
        self.download_tmp_txt()
        self.parse_basic_data()
        self.combine_basic_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        delete_files_in_folder(self.save_tmp_txt_dir, ".csv")


if __name__ == "__main__":
    DownloadFinReport(ProjectDir).main_run()
    
