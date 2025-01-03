from scripts_stock.parse_download_data.fuquan_dfcf_parse import parse_fuquan_data
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.utils.process_folder import delete_files_in_folder
from scripts_stock.utils.logging_set import *
from scripts_stock.utils.data_frame_process import DataFrameProcess
import wget  # 导入wget库
from scripts_stock.utils.json_to_df import read_txt_file
import pandas as pd
import os
import re
import json
from pathlib import Path
import time


# https://data.eastmoney.com/bbsj/202409/yjbb.html
class DownloadProfitReport(ProjectDir):
    def __init__(self, ProjectDir):
        self.page_name = 1
        self.tmp_data_txt_name = ''
        self.save_tmp_txt_dir = ProjectDir.download_profit_data_dir
        self.save_csv_dir = ProjectDir.parse_data_dir_profit_data
        self.download_url = ''
        self.tmp_csv_name = ''

    def download_tmp_txt(self, page_num):
        save_name = os.path.join(self.save_tmp_txt_dir, str(page_num) + ".txt")
        page_num = str(page_num)
        url1 = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112304448470222379983_1734318038997&sortColumns=NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber={page_num}&reportName=RPT_DMSK_FN_INCOME&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)(REPORT_DATE%3D%272024-09-30%27)"
        self.download_url = url1
        wget.download(url1, save_name)
        self.tmp_data_txt_name = save_name
        file_size_bytes = Path(save_name).stat().st_size
        # 转换为KB
        file_size_kb = file_size_bytes / 1024
        return file_size_kb

    def parse_cash_flow_data(self):
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
        df2.to_csv(os.path.join(self.save_csv_dir,
                   "profit_report.csv"), index=False)

    def main_run(self, mode="test"):
        if mode == "test":
            max_loop = 5
        if mode == "all":
            max_loop = 200
        for i in range(1, max_loop):
            try:
                file_size = self.download_tmp_txt(i)
                if file_size < 1:
                    print("\n===========\n")
                    TNLog().info("=========== fin report ============")
                    TNLog().info(f"===== break in {i} loop")
                    break
                else:
                    self.parse_cash_flow_data()
                    time.sleep(10)
            except Exception as e:
                TNLog().error("=========== download_fin_report_error ============")
                TNLog().error(e)
                TNLog().error(self.download_url)
        self.combine_finreport_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        delete_files_in_folder(self.save_tmp_txt_dir, ".csv")
        print("======================================")
        TNLog().info("=finish get fin report data=")
        print("=====================================")
        return


if __name__ == "__main__":
    df_out = DownloadProfitReport(ProjectDir).main_run("test")
    print(df_out)

"""
   column name
     stock_index 	stock_name	TRADE_MARKET_CODE	TRADE_MARKET	SECURITY_TYPE_CODE	SECURITY_TYPE	UPDATE_DATE	REPORTDATE	每股收益	DEDUCT_BASIC_EPS	营业总收入	净利润	净资产收益率	营业总收入同比增长率	净利润同比增长率	每股净资产	每股经营现金流	销售毛利率	营业总收入季度环比增长	净利润季度环比增长	分红	PAYYEAR	行业	ZXGXL	NOTICE_DATE	ORG_CODE	TRADE_MARKET_ZJG	ISNEW	QDATE	DATATYPE	DATAYEAR	DATEMMDD	EITIME	SECUCODE
"""
