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
from scripts_stock.data_base.insert_into_db import insert_df_to_db,read_db_data
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.data_base.db_py_sql import get_all_fuquan_one_stock
from scripts_stock.utils.logging_set import *


"""
need to check new indicators in get_fuquan_index.py
"""

def get_stock_indicator(stock_df_in,if_print=False):
    stock_df = df_to_stock_df(stock_df_in[["open","close","high","low","stock_index","stock_date"]])
    stock_kdj_ind, _ = stock_kdj(stock_df)
    if if_print:
        print(stock_kdj_ind)
    #stock_kdj_ind["stock_index"] = stock_df_in["stock_index"].values[0]
    return stock_kdj_ind

def weekly_data_preprocess(df_raw):
    df_raw['datetime'] = pd.to_datetime(df_raw['date'])
    df_raw['week_group'] = df_raw['datetime'].dt.to_period(
        'W-FRI').apply(lambda r: r.end_time.strftime("%Y-%m-%d"))
    return df_raw

def get_weekly_price_v2(input_df: pd.DataFrame):
    df1 = input_df
    df2 = df1.groupby("week_group").min()
    df3 = df1.groupby("week_group").max()
    df4 = df1.groupby("week_group").last()
    df5 = df1.groupby("week_group").first()
    df2["high"] = df3["high"]
    df2["close"] = df4["close"]
    df2["open"] = df5["open"]
    df2['stock_date'] = df3["date"]
    return df2

class StockIndex(ProjectDir):
    def __init__(self,ProjectDir):
        self.dir_stock_kdj_daily_last = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last.csv")
        self.dir_stock_kdj_daily_all = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_all.csv")
        self.dir_stock_kdj_daily_last5 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last5.csv")
        self.dir_stock_kdj_daily_last60 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last60.csv")
        
        self.dir_stock_kdj_weekly_last = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_weekly_last.csv")
        self.dir_stock_kdj_weekly_all = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_weekly_all.csv")
        self.dir_stock_kdj_weekly_last5 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_weekly_last5.csv")
        self.dir_stock_kdj_weekly_last60 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_weekly_last60.csv")

        self.stock_index_list = GetDataFromDB.get_fuquan_stock_index_all()
        

    def run_indicator(self , GetDataFromDB,if_test="ALL"):
        """
        calculate daily indicator
        """
        ind_list_last = []
        ind_list_last5 = []
        ind_list_all = []
        ind_list_last60 = []
        if if_test=="test":
            stock_index_list_loop = self.stock_index_list[0:5]
        else:
            stock_index_list_loop = self.stock_index_list
    
        for stock_index in stock_index_list_loop:
            try:
                #input_sql_str = get_all_fuquan_one_stock(stock_index)
                df1 = GetDataFromDB.get_fuquan_all_one_stock_df(
                    stock_index).sort_values("date")
                df1["stock_index"] = StringProcess.int_to_stock_index(df1["stock_index"].values[0])
                df1['stock_date'] = df1["date"]
                stock_kdj_ind = get_stock_indicator(df1)
                ind_list_last.append(stock_kdj_ind.iloc[-1])
                ind_list_last5.append(stock_kdj_ind.tail(5))
                ind_list_last60.append(stock_kdj_ind.tail(60))
                ind_list_all.append(stock_kdj_ind)
            except Exception as e:
                TNLog().error("==========================================")
                TNLog().error("==== get KDJ MACD run_indicator error ====")
                TNLog().error(e)
                TNLog().error("==========================================")
                pass

        df_out_last = pd.DataFrame(ind_list_last)
        df_out_all = pd.concat(ind_list_all)
        df_out_last5 = pd.concat(ind_list_last5)
        df_out_last60 = pd.concat(ind_list_last60)
        # dir1 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last.csv")
        df_out_last.round(3).to_csv(self.dir_stock_kdj_daily_last,index=0)  # type: ignore
        df_out_all.round(3).to_csv(self.dir_stock_kdj_daily_all,index=0) # type: ignore
        df_out_last5.round(3).to_csv(self.dir_stock_kdj_daily_last5,index=0) # type: ignore
        df_out_last60.round(3).to_csv(self.dir_stock_kdj_daily_last60,index=0) # type: ignore
        # conn.close()
        # print("======================================")
        # TNLog().info("=finish get stock daily indicators=")
        # print("=====================================")



    def get_weekly_price(self,input_df: pd.DataFrame):
        df1 = input_df
        df2 = df1.groupby(lambda x:math.floor(x/5)).min()
        df3 = df1.groupby(lambda x:math.floor(x/5)).max()
        df4 = df1.groupby(lambda x:math.floor(x/5)).last()
        df5 = df1.groupby(lambda x:math.floor(x/5)).first()
        df2["high"]=df3["high"]
        df2["close"] = df4["close"]
        df2["open"] = df5["open"]
        df2['stock_date'] = df3["date"]
        return df2



    
    def run_indicator_weekly(self,GetDataFromDB,if_test="ALL"):
        """
        calculate weekly indators
        """
        ind_list_last = []
        ind_list_last5 = []
        ind_list_all = []
        ind_list_last60 = []
        stock_index_list_loop = self.stock_index_list[0:5]
        if if_test=="test":
            stock_index_list_loop = self.stock_index_list[0:5]
        else:
            stock_index_list_loop = self.stock_index_list
        for stock_index in stock_index_list_loop:
            try:
                df_raw_v1 = GetDataFromDB.get_fuquan_all_one_stock_df(stock_index)
                df_raw = weekly_data_preprocess(df_raw_v1)
                df_input = get_weekly_price_v2(df_raw)
                stock_kdj_ind = get_stock_indicator(df_input)
                ind_list_last.append(stock_kdj_ind.iloc[-1])
                ind_list_last5.append(stock_kdj_ind.tail(5))
                ind_list_last60.append(stock_kdj_ind.tail(60))
                ind_list_all.append(stock_kdj_ind)
            except Exception as e:
                TNLog().error("=================================================")
                TNLog().error("==== get KDJ MACD run_indicator_weekly error ====")
                TNLog().error(e)
                TNLog().error("=================================================")
                pass

        df_out_last = pd.DataFrame(ind_list_last)
        df_out_all = pd.concat(ind_list_all)
        df_out_last5 = pd.concat(ind_list_last5)
        df_out_last60 = pd.concat(ind_list_last60)
        # dir1 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last.csv")
        df_out_last.round(3).to_csv(self.dir_stock_kdj_weekly_last,index=0)  # type: ignore
        df_out_all.round(3).to_csv(self.dir_stock_kdj_weekly_all,index=0) # type: ignore
        df_out_last5.round(3).to_csv(self.dir_stock_kdj_weekly_last5,index=0) # type: ignore
        df_out_last60.round(3).to_csv(self.dir_stock_kdj_weekly_last60,index=0) # type: ignore
        # conn.close()
        # TNLog().info("======================================")
        # TNLog().info("=finish get stock weekly indicators=")
        # TNLog().info("=====================================")

    def insert_index_data2db(self):
        insert_df_to_db(self.dir_stock_kdj_daily_last,
                        "t_stock_kdj_daily_last", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_daily_all,
                        "t_stock_kdj_daily_all", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_daily_last5,
                        "t_stock_kdj_daily_last5", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_daily_last60,
                        "t_stock_kdj_daily_last60", if_there="replace")
        """
        insert weekly 
        """
        insert_df_to_db(self.dir_stock_kdj_weekly_last,
                        "t_stock_kdj_weekly_last", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_weekly_all,
                        "t_stock_kdj_weekly_all", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_weekly_last5,
                        "t_stock_kdj_weekly_last5", if_there="replace")
        insert_df_to_db(self.dir_stock_kdj_weekly_last60,
                        "t_stock_kdj_weekly_last60", if_there="replace")


if __name__ == '__main__':
    try:
        stock_index_v1 = StockIndex(ProjectDir)
        stock_index_v1.run_indicator(GetDataFromDB)
        stock_index_v1.run_indicator_weekly(GetDataFromDB)
        stock_index_v1.insert_index_data2db()

        TNLog().info("====================================")
        TNLog().info("==== finish KDJ MACD calculation ===")
        TNLog().info("====================================")
    except Exception as e:
        TNLog().error("====================================")
        TNLog().error("==== get KDJ MACD error ====")
        TNLog().error(e)
        print_exception_info()
        TNLog().error("====================================")
