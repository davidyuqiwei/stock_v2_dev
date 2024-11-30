# https://data.eastmoney.com/zjlx/detail.html
import wget  # 导入wget库
import os 
from scripts_stock.cfg.set_dir import *
import pandas as pd
import re
from scripts_stock.utils.json_to_df import read_txt_file
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.download_data.cash_flow.colunm_name import col_fields,keep_col # type: ignore
from scripts_stock.utils.process_folder import delete_files_in_folder
import time
from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.logging_set import *


class DownloadCashFlowData(ProjectDir):
    def __init__(self,ProjectDir):
        self.stock_list = GetDataFromDB.db_get_hs300_list(if_str=True)
        self.save_tmp_txt_dir = ProjectDir.download_data_dir_cash_flow
        self.tmp_data_txt_name = ''
        self.tmp_data_csv_name = os.path.join(self.save_tmp_txt_dir,"tmp_cash_flow_all.csv")
        self.save_csv_dir = ProjectDir.parse_data_dir_cash_flow
        self.base_data = os.path.join(ProjectDir.parse_data_dir_cash_flow,"cash_flow_all_data.csv")

    def download_cash_flow_txt(self,stock_index):
        #if stock_index[0:2] =="60" or stock_index[0:2] == "00":
        if stock_index[0:2] == "60":
            input_stock_index = "1." + stock_index
        if stock_index[0:2] == "00":
            input_stock_index = "0." + stock_index
        url1 = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?cb=jQuery112308863607778096374_1728402940447&lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid={input_stock_index}&_=1728402940448"

        data_name = "cash_flow_" + input_stock_index
        save_name = os.path.join(self.save_tmp_txt_dir, data_name + ".txt")
        wget.download(url1, save_name)
        self.tmp_data_txt_name = save_name
   

    def parse_cash_flow_data(self):
        df1 = read_txt_file(self.tmp_data_txt_name)
        dta = re.findall('klines":\\[(.*)]', df1)
        dta1 = dta[0].split("\",")
        #print(dta1)
        df_list = []
        for k in dta1:
            dta2 = k.replace("\"", "")
            aa = dta2.split(",")
            df_list.append(aa)

        df_out = pd.DataFrame(df_list)
 
        df_out.columns = col_fields
        df_out1 = df_out[keep_col]
        return df_out1
    
    def combine_fuquan_data(self):
        import pandas as pd
        df2 = DataFrameProcess.combine_all_dataframe_in_dir(self.save_tmp_txt_dir)
        df2.to_csv(self.tmp_data_csv_name, index=False)

    def concat_history_data(self):
        df1 = pd.read_csv(self.base_data)
        df2 = pd.read_csv(self.tmp_data_csv_name)
        # 使用 pd.concat 方法垂直堆叠两个 DataFrame
        result = pd.concat([df1, df2], axis=0).drop_duplicates()

        # 重置索引（可选）
        result.reset_index(drop=True, inplace=True)
        result.to_csv(self.base_data,index=False)

    def run(self,mode="test"):   
        stock_list_in = []
        if mode=="test":
            stock_list_in = self.stock_list[0:5]
        if mode=="all":
            stock_list_in = self.stock_list
        for stock_in in stock_list_in:
            try:
                if stock_in[0:2] =="60" or stock_in[0:2] == "00":
                    self.download_cash_flow_txt(stock_in)
                    df_out1 = self.parse_cash_flow_data()
                    df_out1["stock_index"] = stock_in
                    df_out1.to_csv(os.path.join(self.save_tmp_txt_dir,stock_in+".csv"),index=0) # type: ignore
                    time.sleep(10)
            except Exception as e:
                TNLog().error("=========== download_cashflow_error ============")
                TNLog().error(e)
                TNLog().error(stock_in)
                pass
        
        self.combine_fuquan_data()
        self.concat_history_data()
        delete_files_in_folder(self.save_tmp_txt_dir)
        print("======================================")
        TNLog().info("=finish get cashflow data=")
        print("=====================================")

if __name__ == "__main__":
    DownloadCashFlowData(ProjectDir).run("all")