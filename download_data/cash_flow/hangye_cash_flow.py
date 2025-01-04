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

# https://data.eastmoney.com/bkzj/hy.html
class DownloadHangyeCashFlowData(ProjectDir):
    def __init__(self, ProjectDir):
        # self.stock_list = GetDataFromDB.db_get_hs300_list(if_str=True)
        self.save_tmp_txt_dir = ProjectDir.download_data_dir_hangye_cash_flow
        self.tmp_data_txt_name = ''
        self.save_csv_dir = ProjectDir.parse_data_dir_hangye_cash_flow
        self.final_data_name = ""
        print("=========")
        print(ProjectDir.parse_data_dir_hangye_cash_flow)

    def download_bankuai_cash_flow_txt(self):
        url1 = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123037220324330554333_1735126424533&fid=f62&po=1&pz=3000&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
        url2_5days = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309189302985196064_1735128276198&fid=f164&po=1&pz=3000&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13"
        url3_10days = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309189302985196064_1735128276198&fid=f174&po=1&pz=3000&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13"
        url4_stock = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112308050561009937547_1735129017315&fid=f62&po=1&pz=10000&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13%E2%80%98"
        _, yesterday_str,_ = date_today_yesterday()

        url_list = [url1, url2_5days, url3_10days, url4_stock]
        days_list = ["today","5days","10days","stocks"]
        for index,url_in in enumerate(url_list):
            data_name = "hangye_cash_flow_" + \
                days_list[index]+"_" + yesterday_str + ".txt"
            save_name = os.path.join(self.save_tmp_txt_dir, data_name)
            wget.download(url_in, save_name)
            self.tmp_data_txt_name = save_name 
            self.final_data_name = os.path.join(
                self.save_csv_dir, data_name.replace(".txt", ".csv"))
            
            self.parse_cash_flow_data()
            time.sleep(10)
            # print(self.parse_data_dir_bankuai_cash_flow)

    
    def parse_cash_flow_data(self):
        df1 = read_txt_file(self.tmp_data_txt_name)
        dta = re.findall('diff":\\[(.*)]', df1)
        dta1 = dta[0]
        fixed_data = f"[{dta1.replace('},{', '},{')}]"
        # 解析 JSON 字符串
        data_dicts = json.loads(fixed_data)
        df_out1 = pd.DataFrame(data_dicts)

        #df_out1 = pd.DataFrame(df_list)

        #df_out.columns = col_fields
        #df_out1 = df_out[keep_col]
        #print(df_out1)
        df_out1.to_csv(self.final_data_name, index=False)
        return df_out1

    def main_run(self):
        self.download_bankuai_cash_flow_txt()
        # self.parse_cash_flow_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        delete_files_in_folder(self.save_tmp_txt_dir,".csv")

if __name__ == "__main__":
    DownloadHangyeCashFlowData(ProjectDir).main_run()
