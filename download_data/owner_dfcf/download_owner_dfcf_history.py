
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

#   https: // data.eastmoney.com/gdfx/HoldingDetail.html
class DownloadOwnerDFCF(ProjectDir):
    def __init__(self, ProjectDir):
        # self.url = f'https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_EH_FREEHOLDERS&columns=HOLDER_NEW%2CSECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CEND_DATE%2CHOLDER_NAME%2CFREE_HOLDNUM_RATIO%2CHOLDER_MARKET_CAP%2CHOLDER_RANK%2CHOLDER_STATE_NEW%2CCHANGE_RATIO&quoteColumns=&filter=(HOLDER_NEW%3D%2210671586%22)(END_DATE%3D%27{self.input_date}%27)(HOLDER_STATE_NEW%20in%20(%22%E6%96%B0%E8%BF%9B%22%2C%22%E5%8A%A0%E4%BB%93%22%2C%22%E4%B8%8D%E5%8F%98%22%2C%22%E5%87%8F%E4%BB%93%22))&pageNumber=1&pageSize=3000&sortTypes=-1&sortColumns=FREE_HOLDNUM_RATIO&source=Datacenter&client=PC&v=045035569206279935'
        self.save_tmp_txt_dir = ProjectDir.download_data_owner_dfcf
        self.tmp_data_txt_name = ''
        self.save_csv_dir = ProjectDir.parse_data_owner_dfcf
        self.final_data_name = os.path.join(
            self.save_csv_dir, "owner_dfcf_history.csv")

    def get_url(self, input_date, input_page):
        # url = f'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112302156351211279257_1733230393356&sortColumns=UPDATE_DATE%2CSECURITY_CODE%2CHOLDER_RANK&sortTypes=-1%2C1%2C1&pageSize=5000&pageNumber=1&reportName=RPT_F10_EH_FREEHOLDERS&columns=ALL&source=WEB&client=WEB&filter=(HOLDER_NEWTYPE%3D%22QFII%22)(END_DATE%3E%3D%27{input_date}%27)'
        # seasonal, QF2
        url = f'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230419485556059638_1733231638404&sortColumns=UPDATE_DATE%2CSECURITY_CODE%2CHOLDER_RANK&sortTypes=-1%2C1%2C1&pageSize=5000&pageNumber={input_page}&reportName=RPT_F10_EH_FREEHOLDERS&columns=ALL&source=WEB&client=WEB&filter=(HOLDER_NEWTYPE%3D%22QFII%22)(END_DATE%3D%27{input_date}%27)'
        # 社保
        # url2 = f'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123015102862303473752_1734343720380&sortColumns=UPDATE_DATE%2CSECURITY_CODE%2CHOLDER_RANK&sortTypes=-1%2C1%2C1&pageSize=50&pageNumber={input_page}&reportName=RPT_F10_EH_FREEHOLDERS&columns=ALL&source=WEB&client=WEB&filter=(HOLDER_NEWTYPE%3D%22%E7%A4%BE%E4%BF%9D%22)(END_DATE%3E%3D%27{input_date}%27)'
        return url

    def download_tmp_txt(self, input_date, input_page):
        # input_date = '2024-09-30'
        tmp_data_txt_name_in = os.path.join(
            self.save_tmp_txt_dir, "dfcf_owner_" + input_date + "_" + str(input_page) + ".txt")
        wget.download(self.get_url(input_date, input_page),
                      tmp_data_txt_name_in)
        self.tmp_data_txt_name = tmp_data_txt_name_in
        file_size_bytes = Path(self.tmp_data_txt_name).stat().st_size
        # 转换为KB
        file_size_kb = file_size_bytes / 1024
        return file_size_kb

    def parse_owner_dfcf_data(self):
        # input_date = '2024-09-30'
        tmp_data_txt_name = self.tmp_data_txt_name
        df1 = read_txt_file(tmp_data_txt_name)
        dta = re.findall('data":\\[(.*)]', df1)
        dta1 = dta[0]
        fixed_data = f"[{dta1.replace('},{', '},{')}]"
        # 解析 JSON 字符串
        data_dicts = json.loads(fixed_data)
        df = pd.DataFrame(data_dicts)
        print(df)
        tmp_data_csv_name = tmp_data_txt_name.replace(".txt", ".csv")
        df.to_csv(tmp_data_csv_name, index=False)

    def combine_owner_dfcf_data(self):
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
        for i in quater_list:
            for j in range(1, max_page_loop):
                try:
                    self.get_url(i, j)
                    file_size = self.download_tmp_txt(i, j)
                    if file_size < 1:
                        print("\n===========\n")
                        print(i)
                        break
                    else:
                        self.parse_owner_dfcf_data()
                        time.sleep(10)
                except Exception as e:
                    TNLog().error("=========== download_fin_report_error ============")
                    TNLog().error(e)
                    # TNLog().error(self.download_url)
                    pass
        self.combine_owner_dfcf_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        print("======================================")
        TNLog().info("=finish get fin report data=")
        print("=====================================")


if __name__ == "__main__":
    DownloadOwnerDFCF(ProjectDir).main_run("all")
    # DownloadOwnerDFCF(ProjectDir).parse_owner_dfcf_data()
    # print(32)
