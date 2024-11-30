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


def get_data_sql_str(stock_index):
    return f"""SELECT *  FROM prd_t_fuquan_dfcf  where stock_index= {stock_index}"""

def get_fuquan_stock_index_sql_str():
    return """
                SELECT distinct stock_index 
                FROM prd_t_fuquan_dfcf  
            """

def get_stock_indicator(stock_df_in,if_print=False):
    stock_df = df_to_stock_df(stock_df_in[["open","close","high","low","stock_index","stock_date"]])
    stock_kdj_ind, _ = stock_kdj(stock_df)
    if if_print:
        print(stock_kdj_ind)
    #stock_kdj_ind["stock_index"] = stock_df_in["stock_index"].values[0]
    return stock_kdj_ind
# for 
# aaa = get_stock_indicator(df1)
# print(aaa)
class StockIndex(ProjectDir):
    def __init__(self,ProjectDir):
        self.dir_stock_kdj_daily_last = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last.csv")
        self.dir_stock_kdj_daily_all = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_all.csv")
        self.dir_stock_kdj_daily_last5 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last5.csv")
        
    def get_fuquan_stock_index_all(self):
        conn = CommonScript.connect_to_db("test.db")
        cursor = conn.cursor()
        #sql_query_stock_index = 
        stock_list_in = cursor.execute(get_fuquan_stock_index_sql_str()).fetchall()
        stock_index_list = [x[0] for x in stock_list_in]
        conn.close()
        return stock_index_list
    
    def run_indicator(self):
        stock_index_list = self.get_fuquan_stock_index_all()
        conn = CommonScript.connect_to_db("test.db")
        # cursor = conn.cursor()
        ind_list_last = []
        ind_list_last5 = []
        ind_list_all = []
        for stock_index in stock_index_list:
            input_sql_str = get_data_sql_str(stock_index)
            df1 = pd.read_sql_query(input_sql_str, conn)
            df1["stock_index"] = StringProcess.int_to_stock_index(df1["stock_index"].values[0])
            df1['stock_date'] = df1["date"]
            stock_kdj_ind = get_stock_indicator(df1)
            ind_list_last.append(stock_kdj_ind.iloc[-1])
            ind_list_last5.append(stock_kdj_ind.tail(5))
            ind_list_all.append(stock_kdj_ind)
        df_out_last = pd.DataFrame(ind_list_last)
        df_out_all = pd.concat(ind_list_all)
        df_out_last5 = pd.concat(ind_list_last5)
        # dir1 = os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_daily_last.csv")
        df_out_last.round(3).to_csv(self.dir_stock_kdj_daily_last,index=0)  # type: ignore
        df_out_all.round(3).to_csv(self.dir_stock_kdj_daily_all,index=0) # type: ignore
        df_out_last5.round(3).to_csv(self.dir_stock_kdj_daily_last5,index=0) # type: ignore
        conn.close()

    def insert_index_data2db(self):
        insert_df_to_db(self.dir_stock_kdj_daily_last,"t_stock_kdj_daily_last")
        insert_df_to_db(self.dir_stock_kdj_daily_all,"t_stock_kdj_daily_all")
        insert_df_to_db(self.dir_stock_kdj_daily_last5,"t_stock_kdj_daily_last5")




def run_indicator_v2():
    """
    revise this one, monthly kdj macd
    """
    conn = CommonScript.connect_to_db("test.db")
    cursor = conn.cursor()
    #sql_query_stock_index = 
    stock_list_in = cursor.execute(get_fuquan_stock_index_sql_str()).fetchall()
    stock_index_list = [x[0] for x in stock_list_in]  

    ind_list_last = []
    ind_list_last5 = []
    ind_list_all = []
    for stock_index in stock_index_list :
        input_sql_str = get_data_sql_str(stock_index)
        df1 = pd.read_sql_query(input_sql_str, conn)
        df1["stock_index"] = StringProcess.int_to_stock_index(df1["stock_index"].values[0])
        """
        monthly indicators
        """
        df2 = df1.groupby(lambda x:math.floor(x/30)).min()
        df3 = df1.groupby(lambda x:math.floor(x/30)).max()
        df4 = df1.groupby(lambda x:math.floor(x/30)).last()
        df5 = df1.groupby(lambda x:math.floor(x/30)).first()
        df2["high"]=df3["high"]
        df2["close"] = df4["close"]
        df2["open"] = df5["open"]

        # print(df2)
        stock_kdj_ind = new_kdj(df2,kdj_day=9)
        stock_kdj_ind = new_macd(df2,'close')
        ind_list_last.append(stock_kdj_ind.iloc[-1])
        ind_list_last5.append(stock_kdj_ind.tail(5))
        ind_list_all.append(stock_kdj_ind)
    df_out_last = pd.DataFrame(ind_list_last)
    df_out_all = pd.concat(ind_list_all)
    df_out_last5 = pd.concat(ind_list_last5)

    df_out_last.round(3).to_csv(os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_last.csv"),index=0) # type: ignore
    df_out_all.round(3).to_csv(os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_all.csv"),index=0) # type: ignore
    df_out_last5.round(3).to_csv(os.path.join(ProjectDir.analysis_data_dir,"stock_kdj_last5.csv"),index=0) # type: ignore
 

def new_kdj(df,kdj_day=9,k_stat=3,d_stat=3):
    low_list = df['low'].rolling(kdj_day, min_periods=kdj_day).min()
    low_list.fillna(value = df['low'].expanding().min(), inplace = True)
    high_list = df['high'].rolling(kdj_day, min_periods=kdj_day).max()
    high_list.fillna(value = df['high'].expanding().max(), inplace = True)

    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    new_str = '_'.join([str(kdj_day),str(k_stat),str(d_stat)])
    k_col = 'K_'+new_str
    d_col = 'D_'+new_str
    j_col = 'J_'+new_str
    df['K'] = pd.DataFrame(rsv).ewm(com=k_stat-1).mean()
    df[k_col] = pd.DataFrame(rsv).ewm(com=k_stat-1).mean()
    df['D'] = df['K'].ewm(com=d_stat-1).mean()
    df[d_col] = df['K'].ewm(com=d_stat-1).mean()
    df[j_col] = 3 * df['K'] - 2 * df['D']
    return df

def new_macd(df2,col,MACD_EMA_SHORT = 12,MACD_EMA_LONG = 26, MACD_EMA_SIGNAL = 9):
    fast=df2[col].ewm(
                ignore_na=False, span=MACD_EMA_SHORT,
                min_periods=0, adjust=True).mean()
    slow=df2[col].ewm(
                ignore_na=False, span=MACD_EMA_LONG,
                min_periods=0, adjust=True).mean()
    # df2["volume_26"].plot(secondary_y=True, style='r*-')
    # df2["volume_12"].plot(secondary_y=True, style='b*-')
    new_str = '_'.join([str(MACD_EMA_SHORT),str(MACD_EMA_LONG),str(MACD_EMA_SIGNAL)])
    new_macd_col = 'macd_'+new_str
    new_macds_col = 'macds_'+new_str
    new_macdh_col =  'macdh_'+new_str
    df2[new_macd_col] = fast-slow
    df2[new_macds_col] = df2[new_macd_col].ewm(
                ignore_na=False, span=MACD_EMA_SIGNAL,
                min_periods=0, adjust=True).mean()
    df2[new_macdh_col] = (df2[new_macd_col] - df2[new_macds_col])
    return df2

if __name__ == '__main__':
    #print("aaaaa")
    stock_index_v1 = StockIndex(ProjectDir)
    stock_index_v1.run_indicator()
    stock_index_v1.insert_index_data2db()


    #run_indicator_v2()
    """
    
    df1 = pd.read_csv(os.path.join(ProjectDir.download_data_dir_fuquan,"fq_600919.csv"))
    #df2 = df1[["open","close","high","low"]].rolling(30).mean().dropna()
    df2 = df1.groupby(lambda x:math.floor(x/30)).min()
    df3 = df1.groupby(lambda x:math.floor(x/30)).max()
    df4 = df1.groupby(lambda x:math.floor(x/30)).last()
    df5 = df1.groupby(lambda x:math.floor(x/30)).first()
    df2["high"]=df3["high"]
    df2["close"] = df4["close"]
    df2["open"] = df5["open"]
    print(df2)

    # print(df2)
    aa = new_kdj(df2,kdj_day=9)
    aa = new_macd(df2,'close')
    print(aa)
"""
"""

def ttt():
    aa_list = [x for x in os.listdir(ProjectDir.parse_data_dir) if x[0:3] == "fq_"]
    ind_list = []
    for stock_list_in in aa_list:
        #fq_file_name = OutFileName.fuquan_data_name(ProjectDir.parse_data_dir, stock_list_in)
        fq_file_name = os.path.join(ProjectDir.parse_data_dir,stock_list_in)
        df1 = pd.read_csv(fq_file_name)
        df1['stock_date'] = df1["date"]
        del df1["date"]
        #print(df1)
        stock_df = df_to_stock_df(df1)
        stock_kdj_ind, _ = stock_kdj(stock_df)
        # print(stock_kdj_ind)
        stock_kdj_ind["stock_index"] = stock_list_in.split(".")[0]
        # print(df2.round(2))
        # print(df2.iloc[-1])
        ind_list.append(stock_kdj_ind.iloc[-1])
    df_out = pd.DataFrame(ind_list)
    df_out.to_csv(os.path.join(ProjectDir.analysis_data_dir,"stock_kdj.csv"),index=0)

"""
