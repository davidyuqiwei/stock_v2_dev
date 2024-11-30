# -*- coding: utf-8 -*-            
# @Time : 2023/8/23 5:10
# @Author: Davidyu
# @FileName: get_fuquan_index.py
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

"""
get daily return of fuquan data
"""

class StockReturn:
    def __init__(self):
        self.stock_index_list = GetDataFromDB.get_fuquan_stock_index_all()


    def fuquan_hs300_return(self,if_test="ALL"):
        return_list = []
        if if_test=="test":
            stock_index_list_loop = self.stock_index_list[0:5]
        else:
            stock_index_list_loop = self.stock_index_list
        for stock_index in stock_index_list_loop:
            try:
                df1 = GetDataFromDB.get_fuquan_all_one_stock_df(stock_index)
                df1['return_ratio'] = df1['close'] / df1['close'].shift(1)
                df2 = df1[['date','close','return_ratio',"stock_index"]]
                return_list.append(df2)
            except:
                pass
                print(stock_index)
        df_return_all = pd.concat(return_list)
        return df_return_all


if __name__ == '__main__':
    df3 = StockReturn().fuquan_hs300_return().round(3).dropna()
    #print(df3)
    df_save_to_db(input_df=df3,target_table="cal_t_fuquan_daily_return")