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


# https://data.eastmoney.com/bbsj/202409/yjbb.html
class DownloadFinReport(ProjectDir):
    def __init__(self, ProjectDir):
        self.page_name = 1
        self.tmp_data_txt_name = ''
        self.save_tmp_txt_dir = ProjectDir.download_data_dir_fin_report
        self.save_csv_dir = ProjectDir.parse_data_dir_fin_report
        self.download_url = ''
        self.tmp_csv_name = ''
        self.final_data_name = os.path.join(
            self.save_csv_dir, "fin_report_history.csv")

    def download_tmp_txt(self, page_num, report_date):
        page_num = str(page_num)
        save_name = os.path.join(
            self.save_tmp_txt_dir, page_num + "_"+report_date + ".txt")
        url1 = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123043942691880200746_1732599257651&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=3000&pageNumber={page_num}&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE%3D%27{report_date}%27)"
        self.download_url = url1
        wget.download(url1, save_name)
        self.tmp_data_txt_name = save_name
        file_size_bytes = Path(save_name).stat().st_size
        # 转换为KB
        file_size_kb = file_size_bytes / 1024
        return file_size_kb

    def parse_fin_report_data(self):
        df1 = read_txt_file(self.tmp_data_txt_name)
        dta = re.findall('data":\\[(.*)]', df1)
        dta1 = dta[0]
        fixed_data = f"[{dta1.replace('},{', '},{')}]"
        # 解析 JSON 字符串
        data_dicts = json.loads(fixed_data)
        df = pd.DataFrame(data_dicts)
        self.tmp_csv_name = self.tmp_data_txt_name.replace('.txt', '.csv')
        df.to_csv(self.tmp_csv_name, index=False)
        # return df

    def combine_finreport_data(self):
        df2 = DataFrameProcess.combine_all_dataframe_in_dir(
            self.save_tmp_txt_dir)
        df2.to_csv(self.final_data_name, index=False)

    def main_run(self, mode="test"):
        quater_list = get_last_day_of_quarter_range()
        if mode == "test":
            max_page_loop = 2
            quater_list = quater_list[0:2]
        if mode == "all":
            max_page_loop = 200
        print(quater_list)
        for j in quater_list:
            for i in range(1, max_page_loop):
                try:
                    file_size = self.download_tmp_txt(i, j)
                    if file_size < 1:
                        print("\n===========\n")
                        print(i)
                        break
                    else:
                        # self.download_tmp_txt(i,j)
                        self.parse_fin_report_data()
                        time.sleep(10)
                except Exception as e:
                    TNLog().error("=========== download_fin_report_error ============")
                    TNLog().error(e)
                    TNLog().error(self.download_url)
                    pass

        self.combine_finreport_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        print("======================================")
        TNLog().info("=finish get fin report data=")
        print("=====================================")


if __name__ == "__main__":
    DownloadFinReport(ProjectDir).main_run("all")
    # DownloadFinReport(ProjectDir).combine_finreport_data()
