import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
from scripts_stock.data_base.insert_into_db import insert_df_to_db,df_save_to_db
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.data_base.db_py_sql import get_all_fuquan_one_stock
from scripts_stock.utils.logging_set import *


class GetWeeklyPrice:
    stock_index_test = "601398"
    def __init__(self):
        self.stock_list = GetDataFromDB.get_fuquan_stock_index_all()
        #stock_index_test = "601398"
        self.df_out = ""

    def get_weekly_data(self,input_stock_index=stock_index_test):
        df1 = GetDataFromDB.get_fuquan_all_one_stock_df(input_stock_index)
        df2 = df1.groupby(lambda x:math.floor(x/5)).min()
        df3 = df1.groupby(lambda x:math.floor(x/5)).max()
        df4 = df1.groupby(lambda x:math.floor(x/5)).last()
        df5 = df1.groupby(lambda x:math.floor(x/5)).first()
        df2["high"]=df3["high"]
        df2["close"] = df4["close"]
        df2["open"] = df5["open"]
        df2['stock_min_date'] = df2["date"]
        df2['stock_max_date'] = df3["date"]
        
        return df2[["date","open","close","high","low","stock_index","stock_min_date","stock_max_date"]]
    
    def insert_data2db(self):
        df_save_to_db(self.df_out,target_table="cal_t_fuquan_weekly_price")
        print("======================================")
        TNLog().info("=finish fuquan weekly price=")
        print("=====================================")

    
    
    def run(self):
        df_list = []
        for i in self.stock_list:
            df3 = self.get_weekly_data(i)
            df_list.append(df3)
        self.df_out = pd.concat(df_list)
        self.insert_data2db()
        return self
    

if __name__ == '__main__':
    df2 = GetWeeklyPrice().run()
    #print(df2.df_out)